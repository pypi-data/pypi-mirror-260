"""module containing the DownloadApp which will be used when using 
eumdac download **without** the --tailor argument."""
import fnmatch
import shutil
import tempfile
import time

from hashlib import md5
from pathlib import Path
from typing import *

from eumdac.job_id import JobIdentifier
from eumdac.logging import logger
from eumdac.order import Order
from eumdac.product import Product


class DownloadApp:
    def __init__(
        self,
        order: Order,
        datastore: Any,
        integrity: bool = False,
    ) -> None:
        self.order = order
        self.datastore = datastore
        self.check_integrity = integrity
        num_jobs = len(list(self.order.iter_product_info()))
        self.job_identificator = JobIdentifier(num_jobs)

    def run(self) -> bool:
        logger.debug("Starting download(s)")
        return self._run_app()

    def shutdown(self) -> None:
        with self.order._lock:
            return

    def _run_app(self) -> bool:
        with self.order.dict_from_file() as order_d:
            output_dir = order_d["output_dir"]
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True, parents=True)
            dirs = order_d["dirs"]
            onedir = order_d["onedir"]

        (file_patterns,) = self.order.get_dict_entries("file_patterns")
        logger.info(f"Output directory: {Path(output_dir).resolve()}")

        download_success = True

        for product in self.order.get_products(self.datastore):
            self.job_identificator.register(product)
            with self.order.dict_from_file() as order_d:
                state = order_d["products_to_process"][product._id]["server_state"]
            if state == "DONE":
                continue
            if file_patterns:
                entries = product.entries
                filtered_entries = []
                for pattern in file_patterns:
                    matches = fnmatch.filter(entries, pattern)
                    filtered_entries.extend(matches)
                entries = filtered_entries
                for entry in sorted(entries):
                    download_success &= self.download_product(
                        product, entry, output_dir, dirs, onedir
                    )
            else:
                download_success &= self.download_product(product, None, output_dir, dirs, onedir)

            if download_success:
                self.order.update(None, product._id, "DONE")

        return download_success

    def download_product(
        self, product: Product, entry: Optional[str], output_dir: Path, dirs: bool, onedir: bool
    ) -> bool:
        job_id = self.job_identificator.job_id_str(product)

        success = True

        with product.open(entry=entry) as fsrc:
            output = output_dir / fsrc.name
            if dirs or (entry and not onedir):
                # when the dirs or entry flags are used
                # a subdirectory is created
                # to avoid overwriting common files
                # unless the onedir flag has been provided
                output_subdir = output_dir / f"{product}"
                output_subdir.mkdir(exist_ok=True)
                output = output_subdir / fsrc.name

            skip = False

            if output.is_file():
                if self.check_integrity and product.md5 != None:
                    # md5 check
                    md5sum = md5()
                    with output.open("rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            md5sum.update(chunk)
                    if product.md5 == md5sum.hexdigest():
                        logger.info(
                            f"{job_id} Skip {output.name}: file already exists and passes integrity check with MD5 (computed/expected): {md5sum.hexdigest()}/{product.md5}"
                        )
                        skip = True
                    else:
                        logger.info(
                            f"{job_id} Found existing {output.name}, but failed integrity check with MD5 (computed/expected): {md5sum.hexdigest()}/{product.md5}"
                        )
                        skip = False
                else:
                    if self.check_integrity:
                        logger.warn(
                            f"Skipping integrity check: no MD5 metadata found for {output.name}"
                        )
                    logger.info(f"{job_id} Skip {output}, file already exists")
                    skip = True

            if not skip:
                logger.info(f"{job_id} Downloading {output}")
                start = time.perf_counter()

                fully_transferred: bool = False

                with tempfile.TemporaryDirectory(dir=output.parent, suffix=".tmp") as tempdir:
                    tmp = Path(tempdir) / fsrc.name
                    with tmp.open("wb") as fdst:
                        logger.debug(f"Downloading into temporary file: {tmp}")
                        if hasattr(fsrc, "getheader"):
                            content_size_header = fsrc.getheader("Content-Length")  # type:ignore
                            if content_size_header:
                                total = int(content_size_header)
                                transferred = 0
                                while True:
                                    chunk = fsrc.read(1024)
                                    if not chunk:
                                        break
                                    transferred += len(chunk)
                                    fdst.write(chunk)
                                    logger.progress(  # type:ignore
                                        f"{(transferred / (time.perf_counter() - start))/1000000:.2f} MB/s",
                                        transferred,
                                        total,
                                    )
                                logger.progress(  # type:ignore
                                    f"{(transferred / (time.perf_counter() - start))/1000000:.2f} MB/s\n",
                                    transferred,
                                    total,
                                )
                                fully_transferred = transferred == total
                            else:
                                shutil.copyfileobj(fsrc, fdst)
                                fully_transferred = True

                    if not fully_transferred:
                        logger.error(
                            f"{job_id} Product data was not fully transferred, download failed"
                        )
                        success = False
                        return success

                    if self.check_integrity and product.md5 != None:
                        # md5 check
                        md5sum = md5()
                        with tmp.open("rb") as f:
                            for chunk in iter(lambda: f.read(4096), b""):
                                md5sum.update(chunk)

                        if product.md5 == md5sum.hexdigest():
                            logger.info(
                                f"{job_id} Integrity check successful for {output.name} with MD5 (computed/expected): {md5sum.hexdigest()}/{product.md5}"
                            )
                        else:
                            logger.warning(
                                f"{job_id} Integrity check failed for {output.name} with MD5 (computed/expected): {md5sum.hexdigest()}/{product.md5}"
                            )
                            success = False
                    elif self.check_integrity and product.md5 == None:
                        logger.warn(
                            f"Skipping integrity check: no MD5 metadata found for {output.name}"
                        )

                    logger.debug(f"Download finished, moving to final location {output}")
                    shutil.move(str(tmp), output)

        return success
