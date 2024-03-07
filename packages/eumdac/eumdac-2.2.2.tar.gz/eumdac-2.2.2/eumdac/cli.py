"""EUMETSAT Data Access Client"""
from __future__ import annotations

import argparse
import itertools
import os
import pathlib
import re
import fnmatch
import shlex
import shutil
import signal
import stat
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import requests
import yaml
from requests.exceptions import HTTPError

import eumdac
from eumdac import DataStore, DataTailor
from eumdac.collection import SearchResults
from eumdac.config import get_config_dir, get_credentials_path
from eumdac.download_app import DownloadApp
from eumdac.errors import EumdacError
from eumdac.fake import FakeDataStore, FakeDataTailor  # type: ignore
from eumdac.local_tailor import (
    is_online,
    get_api_url,
    get_local_tailor,
    get_tailor_id,
    get_tailor_path,
    new_local_tailor,
    remove_local_tailor,
    all_url_filenames,
)
from eumdac.logging import gen_table_printer, init_logger, logger
from eumdac.order import Order, all_order_filenames, resolve_order
from eumdac.product import Product, ProductError
from eumdac.tailor_app import TailorApp
from eumdac.tailor_models import Chain
from eumdac.token import AccessToken, AnonymousAccessToken
import eumdac.common
from eumdac.cli_mtg_helpers import (
    build_entries_from_coverage,
    pretty_print_entry,
    is_collection_valid_for_coverage,
)

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Callable, Collection, Dict, Iterator, Optional, Tuple, Union

    if sys.version_info < (3, 9):
        from typing import Iterable, Sequence
    else:
        from collections.abc import Iterable, Sequence


def set_credentials(values: Union[str, Sequence[Any], None]) -> None:
    token = eumdac.AccessToken(values)  # type: ignore[arg-type]
    config_dir = get_config_dir()
    config_dir.mkdir(exist_ok=True)
    credentials_path = get_credentials_path()
    credentials_path.touch(mode=(stat.S_IRUSR | stat.S_IWUSR))

    try:
        logger.info(f"Credentials are correct. Token was generated: {token}")
        try:
            with credentials_path.open(mode="w") as file:
                file.write(",".join(values))  # type: ignore[arg-type]
            logger.info(f"Credentials are written to file {credentials_path}")
        except OSError:
            logger.error(
                "Credentials could not be written to {credentials_path}. Please review your configuration."
            )
    except HTTPError as e:
        if e.response.status_code == 401:
            token_url = token.urls.get("token", "token")
            logger.error(
                "The provided credentials are not valid. "
                f"Get your personal credentials at {token_url}",
            )
        else:
            report_request_error(e.response)


class SetCredentialsAction(argparse.Action):
    """eumdac set-credentials entry point"""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        set_credentials(values)
        parser.exit()


def credentials(args: argparse.Namespace) -> None:
    set_credentials((args.ConsumerKey, args.ConsumerSecret))


def token(args: argparse.Namespace) -> None:
    """eumdac token entrypoint"""

    try:
        creds = load_credentials()
    except CredentialsFileNotFoundError as exc:
        raise EumdacError("No credentials found! Please set credentials!") from exc

    try:
        token = AccessToken(creds)
        print(token)
    except HTTPError as e:
        if e.response.status_code == 401:
            token_url = token.urls.get("token", "token")
            logger.error(
                "A token could not be generated with your current credentials. "
                f"Get your credentials from {token_url}",
            )
        report_request_error(e.response)


def describe(args: argparse.Namespace) -> None:
    """eumdac describe entrypoint"""
    datastore = get_datastore(args, anonymous_allowed=True)
    if args.filter and (args.collection or args.product):
        raise ValueError("The -f/--filter flag and can't be used together with -c or -p")
    if args.collection is None and args.product is None:
        filter = str(args.filter).lower() if args.filter else ""
        for collection in datastore.collections:
            collection_str = f"{collection} - {collection.title}"
            if args.filter:
                collection_str_lowercase = collection_str.lower()
                if (filter in collection_str_lowercase) or (
                    fnmatch.fnmatch(collection_str_lowercase, filter)
                ):
                    logger.info(collection_str)
            else:
                logger.info(collection_str)
    elif args.collection is not None and args.product is None:
        collection = datastore.get_collection(args.collection)
        date = collection.metadata["properties"].get("date", "/")
        match = re.match(r"([^/]*)/([^/]*)", date)
        start_date, end_date = match.groups()  # type: ignore[union-attr]
        start_date = start_date or "-"
        end_date = end_date or "now"
        logger.info(f"{collection} - {collection.title}")
        logger.info(f"Date: {start_date} - {end_date}")
        logger.info(collection.abstract)
        logger.info(f'Licence: {"; ".join(collection.metadata["properties"].get("rights", "-"))}')
        logger.info("Search options:")
        for option in collection.search_options.items():
            extra_pad = "\t" if len(option[0]) < 8 else ""
            option_str = f"{option[0]}\t{extra_pad} - {option[1]['title']}"
            if option[1]["options"] and option[1]["options"][0]:
                option_str += f", accepts: {option[1]['options']}"
            cli_param = get_cli_parameter(option[0])
            if cli_param:
                option_str += f", in CLI {cli_param}"
            logger.info(option_str)
    elif args.collection is None and args.product is not None:
        raise ValueError("Please provide a collection id and a product id")
    else:
        noneLabel: str = "(Not available for product)"
        product = datastore.get_product(args.collection, args.product)
        attributes = {
            "Platform": product.satellite,
            "Instrument": product.instrument,
            "Acronym": noneLabel if (not product.acronym) else f"{product.acronym}",
            "Orbit": "GEO" if (not product.orbit_is_LEO) else "LEO",
            "Sensing Start": noneLabel
            if (not product.sensing_start)
            else f"{product.sensing_start.isoformat(timespec='milliseconds')}Z",
            "Sensing End": noneLabel
            if (not product.sensing_end)
            else f"{product.sensing_end.isoformat(timespec='milliseconds')}Z",
            "Size": f"{product.size} KB",
            "Published": noneLabel
            if (not product.ingested)
            else f"{product.ingested.isoformat(timespec='milliseconds')}Z",
            "MD5": noneLabel if (not product.md5) else product.md5,
        }
        lines = [f"{product.collection} - {product}"] + [
            f"{key}: {value}" for key, value in attributes.items()
        ]
        logger.info("\n".join(lines))

        ## Add additional attributes for LEO products
        if product.orbit_is_LEO:
            LEO_attributes = {
                "Timeliness": product.timeliness,
                "Orbit Number": product.orbit_number,
                "Orbit Direction": product.orbit_direction,
                "Relative Orbit": product.relative_orbit,
                "Cycle Number": product.cycle_number,
            }
            lines = [f"{key}: {value}" for key, value in LEO_attributes.items() if value]
            logger.info("\n".join(lines))

        ## Add additional attributes for MTG products
        if product.is_mtg:
            MTG_attributes = {
                "Coverage": noneLabel
                if (not product.region_coverage)
                else f"{product.region_coverage}",
                "Sub-Region": noneLabel
                if (not product.subregion_identifier)
                else f"{product.subregion_identifier}",
                "Repeat Cycle": noneLabel
                if (not product.repeat_cycle)
                else f"{product.repeat_cycle}",
            }
            lines = [f"{key}: {value}" for key, value in MTG_attributes.items() if value]
            logger.info("\n".join(lines))

        if args.verbose:
            verbose_attributes = {
                "Processing Time": noneLabel
                if (not product.processingTime)
                else f"{product.processingTime}",
                "Processor Version": noneLabel
                if (not product.processorVersion)
                else f"{product.processorVersion}",
                "Format": noneLabel if (not product.format) else f"{product.format}",
                "Quality Status": noneLabel
                if (not product.qualityStatus)
                else f"{product.qualityStatus}",
            }
            lines = [f"{key}: {value}" for key, value in verbose_attributes.items() if value]
            logger.info("\n".join(lines))

        if product.entries:
            entries: list[str] = []
            if args.flat:
                entries = sorted(product.entries)
            else:
                entries = get_product_entries_tree(product.entries)
            lines = ["SIP Entries:"] + [f"  {filenames}" for filenames in entries]
            logger.info("\n".join(lines))


def get_product_entries_tree(entries: Iterable[str]) -> list[str]:
    output: list[str] = []
    groups: dict[str, list[str]] = {}
    for entry in sorted(entries):
        if entry.find("/") < 0:
            groups[entry] = []
        else:
            members = entry.split("/", 1)
            if members[0] not in groups:
                groups[members[0]] = [members[1]]
            else:
                groups[members[0]].append(members[1])

    for group in groups:
        is_group: bool = bool(groups[group])
        output.append(f"{'+' if is_group else '-'} {group}{('/' if is_group else '')}")
        if is_group:
            for child in sorted(groups[group]):
                output.append(f"  - {child}")

    return output


def get_cli_parameter(option: str) -> str:
    params = {
        "bbox": "--bbox",
        "geo": "--geometry",
        "title": "--filename",
        "sat": "--satellite",
        "dtstart": "-s, --start",
        "dtend": "-e, --end",
        "publication": "--publication-after, --publication-before",
        "sort": "--sort, --asc, --desc",
        "type": "--product-type, --acronym",
        "timeliness": "--timeliness",
        "orbit": "--orbit",
        "relorbit": "--relorbit",
        "cycle": "--cycle",
    }
    if option in params:
        return params[option]
    else:
        return ""


class ProductIterables:
    """Helper class to manage the length of one or more SearchResults which are iterators"""

    def __init__(
        self,
        query_results: list[SearchResults],
        limit: Optional[int],
        search_query: Dict[str, str],
    ) -> None:
        self.query_results = query_results
        self.search_query = search_query
        self.limit = limit

    def __len__(self) -> int:
        result_lengths = sum(len(pq) for pq in self.query_results)
        if self.limit:
            return min(self.limit, result_lengths)
        return result_lengths

    def __iter__(self) -> Iterator[Product]:
        chained_it = itertools.chain(*self.query_results)
        if self.limit:
            return itertools.islice(chained_it, self.limit)
        return chained_it

    def __contains__(self, item: object) -> bool:
        raise NotImplementedError()


def _get_args_search_params(args: argparse.Namespace) -> list[str]:
    search_params_in_args = []
    vargs = vars(args)
    for param in [
        "dtstart",
        "dtend",
        "time_range",
        "publication_after",
        "publication_before",
        "sort",
        "bbox",
        "geo",
        "sat",
        "sort",
        "cycle",
        "orbit",
        "relorbit",
        "title",
        "timeliness",
    ]:
        if param in vargs and vargs[param]:
            search_params_in_args.append(param)
    return search_params_in_args


def _get_query_paging_params(query: str) -> list[str]:
    return [
        member
        for member in query.split("&")
        if member.split("=")[0] in ["format", "si", "c", "id", "pw"]
    ]


def _search(args: argparse.Namespace) -> Tuple[Collection[Product], int, str]:
    """given search query arguments will return the list of matching products"""
    datastore = get_datastore(args, anonymous_allowed=True)
    query_results = []
    products: Collection[Product]
    num_products: int

    if args.query:
        extra_search_params = _get_args_search_params(args)
        if extra_search_params:
            logger.warning(
                f"The following search parameters have been ignored in favour of the opensearch query: {', '.join(extra_search_params)}"
            )
        paging_params = _get_query_paging_params(args.query[0])
        if paging_params:
            logger.warning(
                f"The following opensearch terms have been ignored: {', '.join(paging_params)}"
            )
        search_results = datastore.opensearch(args.query[0])
        collection_id = str(search_results.collection)
        query_results.append(search_results)
        products = ProductIterables(query_results, args.limit, search_results.query)
        # Check the number of products to execute the search
        num_products = len(products)
    else:
        # See https://docs.opengeospatial.org/is/13-026r9/13-026r9.html#20 for the mathematical notation expected by the publication filter
        if args.publication_after and args.publication_before:
            publication = f"[{args.publication_after.isoformat(timespec='milliseconds')}Z,{args.publication_before.isoformat(timespec='milliseconds')}Z]"
        elif args.publication_after:
            publication = f"[{args.publication_after.isoformat(timespec='milliseconds')}Z"
        elif args.publication_before:
            publication = f"{args.publication_before.isoformat(timespec='milliseconds')}Z]"
        else:
            publication = None

        sort_query = None
        if args.sort:
            if args.sort == "ingestion":
                sort_prefix = "publicationDate,,"
            elif args.sort == "sensing":
                sort_prefix = "start,time,"
            else:
                raise EumdacError("Unexpected sorting argument: {args.sort}")
            direction = 1
            if args.desc:
                direction = 0
            if args.asc:
                direction = 1
            sort_query = f"{sort_prefix}{direction}"

        _query = {
            "dtstart": args.dtstart,
            "dtend": args.dtend,
            "publication": publication,
            "bbox": args.bbox,
            "geo": args.geo,
            "sat": args.sat,
            "sort": sort_query,
            "cycle": args.cycle,
            "orbit": args.orbit,
            "relorbit": args.relorbit,
            "title": args.filename,
            "timeliness": args.timeliness,
            "type": args.product_type,
        }

        query = {key: value for key, value in _query.items() if value is not None}
        bbox = query.pop("bbox", None)
        if bbox is not None:
            query["bbox"] = ",".join(map(str, bbox))

        products = []
        num_products = 0
        for collection_id in args.collection:
            try:
                collection = datastore.get_collection(collection_id)
                query_results.append(collection.search(**query))
                products = ProductIterables(query_results, args.limit, query)
                # Check the number of products to execute the search
                num_products = len(products)
            except Exception as err:
                logger.debug(f"Search failed, checking if collection id {collection_id} is valid")
                datastore.check_collection_id(collection_id)
                raise

    return products, num_products, collection_id


def _parse_timerange(args: argparse.Namespace) -> Tuple[datetime, datetime]:
    """
    Parses the time range provided as arguments.

    This function receives the parsed command-line arguments as an argparse.Namespace object.
    The function checks if the `--time-range` argument is used, and if so, it parses the start
    and end times from the provided time range. The start time defaults to the beginning of the day
    and the end time defaults to the end of the day if specific times are not provided.

    If the `--time-range` argument is not used, the function uses the `--start` (`dtstart`) and
    `--end` (`dtend`) arguments instead. If `--time-range` is used in combination with
    `--start` or `--end`, a ValueError is raised.

    Parameters:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        tuple: A tuple of two datetime objects representing the start and end of the time range.

    Raises:
        ValueError: If both --time-range and --start/--end are used.
    """
    if args.time_range and (args.dtstart or args.dtend):
        raise ValueError("You can't combine --time-range and --start/--end.")

    if args.time_range:
        start, end = args.time_range
        start = parse_isoformat_beginning_of_day_default(start)
        end = parse_isoformat_end_of_day_default(end)
    else:
        start = args.dtstart
        end = args.dtend
    return start, end


def search(args: argparse.Namespace) -> None:
    """eumdac search entrypoint"""
    products_query, products_count, _ = _search(args)

    limit = args.limit or 10000
    products = itertools.islice(products_query, limit)
    if products_count < 1:
        logger.error(f"No products were found for the given search parameters")
        return
    if products_count > limit:
        # show a warning through stderr only when more than 10000
        # products would be shown and limit keyword is not used.
        logger.warning(f"By default, only 10000 of {products_count} products are displayed.")
        logger.warning("Please use --limit to increase the number of products if necessary.")
    if products_count > 10000:
        logger.error(
            "Notice: EUMETSATs DataStore APIs allow a maximum of 10.000 items in a single request. If more than 10.000 items are needed, please split your requests."
        )
    for product in products:
        CRLF = "\r\n"
        logger.info(str(product).replace(CRLF, "-"))


class AngrySigIntHandler:
    """class that will block a SigInt `max_block` times before exiting the program"""

    def __init__(self, max_block: int = 3) -> None:
        self.max_block = max_block
        self.ints_received = 0

    def __call__(self, *args: Any) -> None:
        self.ints_received += 1
        if self.ints_received > self.max_block:
            logger.warning("Forced shut down.")
            sys.exit(1)
        logger.warning(
            "Currently shutting down. "
            f"Interrupt {self.max_block - self.ints_received + 1} "
            "more times to forcefully shutdown."
        )


def safe_run(
    app: Any,
    collection: Optional[str] = None,
    num_products: int = -1,
    keep_order: bool = False,
) -> bool:
    """wrapper around app.run() for exception handling and logging"""

    if num_products < 0:
        num_products = len(list(app.order.iter_product_info()))
        plural = "" if num_products == 1 else "s"
        logger.info(f"Processing {num_products} product{plural}.")
    (chain,) = app.order.get_dict_entries("chain")
    if chain:
        plural = "" if num_products == 1 else "s"
        logger.info(f"Product{plural} will be customized with the following parameters:")
        for line in yaml.dump(chain).splitlines():
            logger.info(f"   {line}")

    logger.info(f"Using order: {app.order}")
    try:
        success = app.run()
        if not keep_order and app.order.status() == "DONE":
            logger.info(f"Removing successfully finished order {app.order}")
            app.order.delete()
        return success
    except KeyboardInterrupt:
        signal.signal(signal.SIGINT, AngrySigIntHandler())
        logger.info("Received request to shut down.")
        logger.info("Finishing Threads..")
        app.shutdown()
        logger.info("Resume this order with the following command:")
        logger.info(f"$ eumdac order resume {app.order}")
        raise
    except ProductError:
        if collection:
            app.datastore.check_collection_id(collection)
            raise
        else:
            raise
    except Exception as e:
        logger.critical(f"Unexpected exception: {str(e)}")
        raise


def download(args: argparse.Namespace) -> None:
    """eumdac download entrypoint"""
    datastore = get_datastore(args)
    products: Collection[Product]
    collection: str

    if args.query:
        # Search using a query
        products, products_count, collection = _search(args)
    else:
        # Search using CLI parameters or product
        if not args.collection or len(args.collection) > 1:
            raise ValueError("Please provide a (single) collection.")

        if args.product:
            if args.dtstart or args.dtend:
                logger.warning(
                    "Parameter(s) for filtering using sensing time ignored as specific product ID was given."
                )
            if args.publication_after or args.publication_before:
                logger.warning(
                    "Parameter(s) for filtering using sensing time ignored as specific product ID was given."
                )
            if args.bbox or args.geo:
                logger.warning(
                    "Parameter(s) for filtering using spatial geometry ignored as specific product ID was given."
                )
            if args.sat:
                logger.warning(
                    "Parameter for filtering using satellite/platform ignored as specific product ID was given."
                )
            if args.product_type:
                logger.warning(
                    "Parameter for filtering using product type/acronym ignored as specific product ID was given."
                )
            if args.cycle or args.orbit or args.relorbit:
                logger.warning(
                    "Parameter(s) for filtering using acquisition parameters ignored as specific product ID was given."
                )
            if args.filename:
                logger.warning(
                    "Parameter for filtering using filename/title ignored as specific product ID was given."
                )
            if args.timeliness:
                logger.warning(
                    "Parameter for filtering using timeliness ignored as specific product ID was given."
                )

        collection = args.collection[0]

        if args.product:
            products = [datastore.get_product(collection, pid) for pid in args.product]
            products_count = len(products)
        else:
            products, products_count, _ = _search(args)

    products_count = len(products)

    if args.integrity:
        if args.download_coverage:
            logger.warn("Ignoring --integrity flag as --download-coverage was provided.")
            args.integrity = False
        elif args.entry:
            logger.warn("Ignoring --integrity flag as --entry was provided.")
            args.integrity = False

    if products_count > 10000:
        logger.info(f"Processing 10000 out of the total {products_count} products.")
        products = itertools.islice(products, 10000)  # type: ignore
        products_count = 10000
        logger.error(
            "Notice: EUMETSATs DataStore APIs allow a maximum of 10.000 items in a single request. If more than 10.000 items are needed, please split your requests."
        )
    else:
        plural = "" if products_count == 1 else "s"
        logger.info(f"Processing {products_count} product{plural}.")

    if products_count >= 10 and not args.yes:
        user_in = input("Do you want to continue (Y/n)? ")
        if user_in.lower() == "n":
            return

    order = Order()

    try:
        query = products.search_query  # type: ignore
    except AttributeError:
        query = None

    if args.download_coverage:
        # Check that a valid, pdu-based collection has been provided (MTG FCI 1C)
        if not is_collection_valid_for_coverage(collection):
            logger.error(f"Collection {collection} does not support coverage area downloads.")
            logger.error(
                f"Remove coverage: {args.download_coverage} parameter or provide a different collection."
            )
            return
        # Complain about entry being provided with coverage
        if args.entry:
            logger.warn(
                f"The provided --entry values {args.entry} will be discarded in favour of the coverage parameter."
            )
        # Prepare multi-entry considering coverage
        args.entry, expected = build_entries_from_coverage(args.download_coverage)
        # Check first if all the chunks are in the product
        if args.entry:
            for product in products:
                matches = []
                for pattern in args.entry:
                    matches.extend(fnmatch.filter(product.entries, pattern))
                logger.info(f"{len(matches)} entries will be downloaded for {product}")
                if args.verbose:
                    logger.info(
                        "\n".join([f"  - {pretty_print_entry(match)}" for match in sorted(matches)])
                    )
                if len(matches) < expected:
                    logger.warn(
                        f"Warning: not all the expected chunks could be found: found {len(matches)} out of {expected}"
                    )

    if args.tailor and args.chain:
        raise ValueError("Please provide either a tailor file or chain yaml string!")
    elif args.tailor or args.chain:
        chain_config = ""
        if args.tailor:
            chain_config = args.tailor
        elif args.chain:
            chain_config = args.chain
        if chain_config.endswith(".yml") or chain_config.endswith(".yaml"):
            with open(chain_config, "r") as file:
                try:
                    chain = yaml.safe_load(file)
                except:
                    logger.error("YAML file is corrupted. Please, check the YAML syntax.")
                    sys.exit()
        else:
            chain_config = chain_config.strip()
            if not chain_config.startswith("{"):
                chain_config = "{" + chain_config + "}"
            try:
                chain = yaml.safe_load(chain_config)
            except:
                logger.error("YAML string is corrupted. Please, check the YAML syntax.")
                sys.exit()
        chain = Chain(**chain)
        order.initialize(
            chain,
            products,
            Path(args.output_dir),
            args.entry,
            query,
            args.dirs,
            args.onedir,
            args.no_warning_logs,
        )
        datatailor = get_datatailor(args)
        app: Any = TailorApp(order, datastore, datatailor)
    else:
        order.initialize(
            None,
            products,
            Path(args.output_dir),
            args.entry,
            query,
            args.dirs,
            args.onedir,
            args.no_warning_logs,
        )
        app = DownloadApp(order, datastore, integrity=args.integrity)

    if args.dirs:
        logger.warn("A subdirectory per product will be created, as per the --dirs option")
    if args.onedir:
        logger.warn("Subdirectories per product will not be created, as per the --onedir option")

    success = safe_run(
        app, collection=collection, num_products=products_count, keep_order=args.keep_order
    )
    if not success:
        raise EumdacError("Downloads didn't finish successfully")


def order(args: argparse.Namespace) -> None:
    """eumdac order entrypoint"""
    if args.order_command == "list":
        filenames = list(all_order_filenames())
        logger.info(f"Found {len(filenames)} order(s):")
        table_printer = gen_table_printer(
            logger.info,
            [
                ("Order ID", 15),
                ("Created on", 10),
                ("Products", 8),
                ("Tailor", 6),
                ("Status", 15),
                ("Collection", 28),
            ],
            column_sep="  ",
        )
        for filename in filenames:
            try:
                order = Order(filename)
                with order.dict_from_file() as order_d:
                    table_printer(
                        [
                            filename.stem,  # order_id
                            filename.stem.split("#")[0],  # created
                            str(len(order_d["products_to_process"])),  # products
                            "Yes" if order_d["type"] == "tailor" else "No",  # tailor
                            order.status(),  # status
                            ", ".join(order.collections()),  # collection
                        ]
                    )
            except (EumdacError, KeyError, yaml.scanner.ScannerError):
                logger.error(f"{filename.stem}  is corrupted.")
        return

    order_name = args.order_id
    order = resolve_order(order_name)

    if args.order_command == "status":
        logger.info(order.pretty_string(print_products=args.verbose))
        if not args.verbose:
            logger.info("")
            logger.info("Use the -v flag to see more details")
        return

    if args.order_command == "restart":
        order.reset_states()

    if args.order_command == "delete":
        if args.all:
            filenames = list(all_order_filenames())
            logger.info(f"Deleting {len(filenames)} order(s):")
            for filename in filenames:
                try:
                    order = Order(filename)
                    order.delete()
                    logger.info(f"Order {order} successfully deleted.")
                except Exception as err:
                    logger.error(f"Unable to delete order {order} due to: {err}")
        elif order._order_file.is_file():
            delete = True
            if not args.yes:
                user_in = input(f"Are you sure to delete order {order_name} (Y/n)?")
                delete = not (user_in.lower() == "n")
            if delete:
                try:
                    order.delete()
                    logger.info(f"Order {order_name} successfully deleted.")
                except:
                    logger.warning(f"Order {order_name} can't be deleted.")
            else:
                logger.info(f"Order {order_name} wasn't deleted.")
        else:
            logger.info(f"Order {order_name} doesn't exist.")
        sys.exit()

    if not order._order_file.is_file():
        logger.info(f"Order {order_name} doesn't exist.")
        sys.exit()

    (typ,) = order.get_dict_entries("type")
    if typ == "download":
        if args.integrity and order.get_dict_entries("file_patterns"):
            logger.warn("Ignoring --integrity flag as Order is configured to download entries.")
            args.integrity = False
        app: Any = DownloadApp(order, get_datastore(args), integrity=args.integrity)

    elif typ == "tailor":
        if order.all_done():
            logger.info("Order already completed")
            return
        app = TailorApp(order, get_datastore(args), get_datatailor(args))

    else:
        raise Exception(f"Unknown Order Type: {typ}")

    success = safe_run(app, keep_order=args.keep_order)
    if not success:
        raise EumdacError("Process didn't finish successfully")


def local_tailor(args: argparse.Namespace) -> None:
    """eumdac config entrypoint"""
    if args.local_tailor_command == "set":
        old_url = ""
        try:
            try:
                old_url = get_api_url(get_tailor_path(args.localtailor_id[0]))
            except:
                pass

            local_tailor_config_path = new_local_tailor(
                args.localtailor_id[0], args.localtailor_url[0]
            )

            logger.info(
                f"Local tailor instance {get_tailor_id(local_tailor_config_path)} is configured with the following address: {get_api_url(local_tailor_config_path)}"
            )
            if old_url:
                logger.warning(
                    f"This replaces the previous address for {get_tailor_id(local_tailor_config_path)}: {old_url}"
                )
            if not is_online(local_tailor_config_path):
                logger.warning(
                    "Note that the provided local-tailor instance address is unavailable at the moment"
                )

        except EumdacError as e:
            logger.error(
                f"The provided address {args.localtailor_url[0]} appears to be invalid: {e}"
            )
            # Don't remove existing instances
            if not old_url:
                remove_local_tailor(args.localtailor_id[0])

    elif args.local_tailor_command == "remove":
        try:
            local_tailor_config_path = get_tailor_path(args.localtailor_id[0])
            logger.info(
                f"Local tailor instance {get_tailor_id(local_tailor_config_path)} is removed"
            )
            remove_local_tailor(args.localtailor_id[0])
        except EumdacError as e:
            logger.error(f"Could not remove local tailor instance: {e}")

    elif args.local_tailor_command == "show":
        table_printer = gen_table_printer(logger.info, [("Name", 10), ("URL", 40), ("Status", 8)])
        local_tailor_config_path = get_tailor_path(args.localtailor_id[0])
        table_printer(
            [
                get_tailor_id(local_tailor_config_path),
                get_api_url(local_tailor_config_path),
                "ONLINE" if is_online(local_tailor_config_path) else "OFFLINE",
            ]
        )

    elif args.local_tailor_command == "instances":
        table_printer = gen_table_printer(logger.info, [("Name", 10), ("URL", 40), ("Status", 8)])
        for filepath in all_url_filenames():
            if filepath.exists():
                line = [
                    get_tailor_id(filepath),
                    get_api_url(filepath),
                    "ONLINE" if is_online(filepath) else "OFFLINE",
                ]
                table_printer(line)

    else:
        raise EumdacError(f"Unsupported clear command: {args.local_tailor_command}")


def get_datastore(args: argparse.Namespace, anonymous_allowed: bool = False) -> Any:
    """get an instance of DataStore"""
    if args.test:
        return FakeDataStore()
    try:
        creds = load_credentials()
    except CredentialsFileNotFoundError as exc:
        if anonymous_allowed:
            creds = None
        else:
            raise EumdacError("No credentials found! Please set credentials!") from exc

    if creds is None:
        token: Any = AnonymousAccessToken()
    else:
        token = AccessToken(creds)
    return DataStore(token)


def get_datatailor(args: argparse.Namespace) -> Any:
    """get an instance of DataTailor"""
    if args.test:
        logger.info("Using Fake DataTailor instance")
        return FakeDataTailor()
    if args.local_tailor:
        logger.info(f"Using Data Tailor Standalone instance: {args.local_tailor}")
        return get_local_tailor(args.local_tailor)
    try:
        creds = load_credentials()
    except CredentialsFileNotFoundError as exc:
        raise EumdacError("No credentials found! Please set credentials!") from exc
    token = AccessToken(creds)
    logger.info("Using Data Tailor Web Service")
    return DataTailor(token)


def load_credentials() -> Iterable[str]:
    """load the credentials and do error handling"""
    credentials_path = get_credentials_path()
    try:
        content = credentials_path.read_text()
    except FileNotFoundError as exc:
        raise CredentialsFileNotFoundError(str(credentials_path)) from exc
    match = re.match(r"(\w+),(\w+)$", content)
    if match is None:
        raise EumdacError(f'Corrupted file "{credentials_path}"! Please reset credentials!')
    return match.groups()


def tailor_post_job(args: argparse.Namespace) -> None:
    """eumdac tailor post entrypoint"""
    from eumdac.tailor_models import Chain

    datastore = get_datastore(args)
    datatailor = get_datatailor(args)
    collection_id = args.collection
    product_ids = args.product
    chain_config = args.chain

    if not args.collection or not args.product or not args.chain:
        raise ValueError("Please provide collection ID, product ID and a chain file!")
    if chain_config.endswith(".yml") or chain_config.endswith(".yaml"):
        with open(chain_config, "r") as file:
            try:
                chain = yaml.safe_load(file)
            except:
                logger.error("YAML file is corrupted. Please, check the YAML syntax.")
                sys.exit()
    else:
        chain_config = chain_config.strip()
        if not chain_config.startswith("{"):
            chain_config = "{" + chain_config + "}"
        try:
            chain = yaml.safe_load(chain_config)
        except:
            logger.error("YAML string is corrupted. Please, check the YAML syntax.")
            sys.exit()
    chain = Chain(**chain)
    products = [datastore.get_product(collection_id, product_id) for product_id in product_ids]
    try:
        customisation = datatailor.new_customisations(products, chain=chain)
        jobidsToStr = "\n".join([str(jobid) for jobid in customisation])
        logger.info("Customisation(s) has been started.")
        logger.info(jobidsToStr)
    except requests.exceptions.HTTPError as exception:
        messages = {
            400: "Collection ID and/or Product ID does not seem to be a valid. See below:",
            500: "There was an issue on server side. See below:",
            0: "An error occurred. See below:",
            -1: "An unexpected error has occurred.",
        }
        report_request_error(exception.response, None, messages=messages)


def tailor_list_customisations(args: argparse.Namespace) -> None:
    """eumdac tailor list entrypoint"""
    datatailor = get_datatailor(args)
    try:
        customisations = datatailor.customisations
        if not customisations:
            logger.error("No customisations available")
        else:
            table_printer = gen_table_printer(
                logger.info,
                [("Job ID", 10), ("Status", 8), ("Product", 10), ("Creation Time", 20)],
            )
            for customisation in datatailor.customisations:
                line = [
                    str(customisation),
                    customisation.status,
                    customisation.product_type,
                    str(customisation.creation_time),
                ]
                table_printer(line)
    except requests.exceptions.HTTPError as exception:
        report_request_error(exception.response)


def tailor_show_status(args: argparse.Namespace) -> None:
    """eumdac tailor status entrypoint"""
    datatailor = get_datatailor(args)
    if args.verbose:
        table_printer = gen_table_printer(
            logger.info,
            [("Job ID", 10), ("Status", 8), ("Product", 10), ("Creation Time", 20)],
        )
        for customisation_id in args.job_ids:
            try:
                customisation = datatailor.get_customisation(customisation_id)
                line = [
                    str(customisation),
                    customisation.status,
                    customisation.product_type,
                    str(customisation.creation_time),
                ]
                table_printer(line)
            except requests.exceptions.HTTPError as exception:
                report_request_error(exception.response, customisation_id)
    else:
        for customisation_id in args.job_ids:
            try:
                customisation = datatailor.get_customisation(customisation_id)
                logger.info(customisation.status)
            except requests.exceptions.HTTPError as exception:
                report_request_error(exception.response, customisation_id)


def tailor_get_log(args: argparse.Namespace) -> None:
    """eumdac tailor log entrypoint"""
    datatailor = get_datatailor(args)
    try:
        customisation = datatailor.get_customisation(args.job_id)
        logger.info(customisation.logfile)
    except requests.exceptions.HTTPError as exception:
        report_request_error(exception.response, args.job_id)


def tailor_quota(args: argparse.Namespace) -> None:
    """eumdac tailor quota entrypoint"""
    datatailor = get_datatailor(args)
    user_name = datatailor.user_info["username"]
    quota_info = datatailor.quota["data"][user_name]
    is_quota_active = quota_info["disk_quota_active"]

    logger.info(f"Usage: {round(quota_info['space_usage'] / 1024, 1)} Gb")
    if is_quota_active:
        logger.info(f"Percentage: {round(quota_info['space_usage_percentage'], 1)}%")
        if args.verbose:
            logger.info(f"Available: {round(quota_info['user_quota'] / 1024, 1)} Gb")
    else:
        logger.info("No quota limit set in the system")

    if args.verbose:
        logger.info(f"Workspace usage: {round(quota_info['workspace_dir_size'] / 1024, 1)} Gb")
        logger.info(f"Logs space usage: {round(quota_info['log_dir_size'], 3)} Mb")
        logger.info(f"Output usage: {round(quota_info['output_dir_size'], 1)} Mb")
        logger.info(f"Jobs: {quota_info['nr_customisations']}")


def tailor_delete_jobs(args: argparse.Namespace) -> None:
    """eumdac tailor delete entrypoint"""
    datatailor = get_datatailor(args)
    for customisation_id in args.job_ids:
        customisation = datatailor.get_customisation(customisation_id)
        try:
            customisation.delete()
            logger.info(f"Customisation {customisation_id} has been deleted.")
        except requests.exceptions.HTTPError as exception:
            if exception.response.status_code >= 400:
                report_request_error(exception.response, customisation_id)


def tailor_cancel_jobs(args: argparse.Namespace) -> None:
    """eumdac tailor cancel entrypoint"""
    datatailor = get_datatailor(args)

    for customisation_id in args.job_ids:
        customisation = datatailor.get_customisation(customisation_id)
        try:
            customisation.kill()
            logger.info(f"Customisation {customisation_id} has been cancelled.")
        except requests.exceptions.HTTPError as exception:
            messages = {
                400: f"{customisation_id} is already cancelled or job id is invalid. See below:",
                500: "There was an issue on server side. See below:",
                0: "An error occurred. See below:",
                -1: "An unexpected error has occurred.",
            }
            report_request_error(exception.response, None, messages=messages)


def tailor_clear_jobs(args: argparse.Namespace) -> None:
    """eumdac tailor clear entrypoint"""
    datatailor = get_datatailor(args)

    jobs_to_clean = args.job_ids

    if args.all and len(args.job_ids) > 0:
        logger.info(
            "All flag provided. Ignoring the provided customization IDs and clearing all jobs"
        )

    if args.all:
        # Fetch all job ids
        jobs_to_clean = datatailor.customisations

    for customisation in jobs_to_clean:
        # If we are provided a job id, get the customisation
        if isinstance(customisation, str):
            customisation_id = customisation
            customisation = datatailor.get_customisation(customisation)
        else:
            customisation_id = customisation._id

        try:
            if (
                customisation.status == "QUEUED"
                or customisation.status == "RUNNING"
                or customisation.status == "INACTIVE"
            ):
                customisation.kill()
                logger.info(f"Customisation {customisation_id} has been cancelled.")
        except requests.exceptions.HTTPError as exception:
            messages = {
                400: f"{customisation_id} is already cancelled or job id is invalid. See below:",
                500: "There was an issue on server side. See below:",
                0: "An error occurred. See below:",
                -1: "An unexpected error has occurred.",
            }
            report_request_error(exception.response, None, messages=messages)

        try:
            customisation.delete()
            logger.info(f"Customisation {customisation_id} has been deleted.")
        except requests.exceptions.HTTPError as exception:
            report_request_error(exception.response, customisation_id)


def tailor_download(args: argparse.Namespace) -> None:
    """eumdac tailor download entrypoint"""
    creds = load_credentials()
    token = AccessToken(creds)
    customisation = eumdac.datatailor.Customisation(args.job_id, datatailor=DataTailor(token))
    results: Iterable[str] = customisation.outputs
    logger.info(f"Output directory: {os.path.abspath(args.output_dir)}")
    if not os.path.exists(args.output_dir):
        logger.info(f"Output directory {args.output_dir} does not exist. It will be created.")
        os.makedirs(args.output_dir)
    # Download all the output files into the output path
    logger.info(f"Downloading {len(results)} output products")  # type: ignore
    for result in results:
        product_name = os.path.basename(result)
        logger.info("Downloading " + product_name)

        with tempfile.TemporaryDirectory(dir=args.output_dir, suffix=".tmp") as tempdir:
            tmp_prod_p = Path(tempdir) / str(product_name)
            with tmp_prod_p.open("wb") as tmp_prod:
                with customisation.stream_output_iter_content(result) as chunks:
                    for chunk in chunks:
                        tmp_prod.write(chunk)
            shutil.move(str(tmp_prod_p), str(args.output_dir) + "/" + product_name)
            logger.info(f"{product_name} has been downloaded.")


def report_request_error(
    response: requests.Response,
    cust_id: Optional[str] = None,
    messages: Optional[Dict[int, str]] = None,
) -> None:
    """helper function report requests errors to the user"""
    if messages is not None:
        _messages = messages
    else:
        _messages = {
            400: "There was an issue on client side. See below:",
            500: "There was an issue on server side. See below:",
            0: "An error occurred. See below:",
            -1: "An unexpected error has occurred.",
        }
        if cust_id is not None:
            _messages[400] = f"{cust_id} does not seem to be a valid job id. See below:"

    def _message_func(status_code: Optional[int] = None) -> str:
        try:
            if not status_code:
                return _messages[-1]

            if 400 <= status_code < 500:
                return _messages[400]

            elif status_code >= 500:
                return _messages[500]
            return _messages[0]
        except KeyError:
            return "Error description not found"
        return "Unexpected error"

    message = _message_func(response.status_code)

    logger.error(message)
    logger.error(f"{response.status_code} - {response.text}")


class HelpAction(argparse.Action):
    """eumdac tailor/search/download/order -h entrypoint"""

    def __call__(self, parser: argparse.ArgumentParser, *args: Any, **kwargs: Any) -> None:
        # Print the help if the command has 2 args,
        # meaning it's just $ eumdac tailor
        if len(sys.argv) == 2:
            parser.print_help()
            parser.exit()


def parse_isoformat(input_string: str, time_default: str = "start") -> datetime:
    """helper function to provide a user readable message when argparse encounters
    a wrongly formatted date"""
    time_defaults = {
        "start": "00:00:00",
        "end": "23:59:59",
    }
    try:
        _default_time = time_defaults[time_default]
    except KeyError as exc:
        raise ValueError(f"Unexpected time_default: '{time_default}'") from exc

    if "T" not in input_string:
        input_string += f"T{_default_time}"
        if time_default == "end":
            logger.warning(f"As no time was given for end date, it was set to {input_string}.")

    try:
        return datetime.fromisoformat(input_string)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "The format of the provided date was not recognized. "
            "Expecting YYYY-MM-DD[THH[:MM[:SS]]]"
        ) from exc


def parse_isoformat_beginning_of_day_default(input_string: str) -> datetime:
    """helper function to provide to parse start dates"""
    return parse_isoformat(input_string, time_default="start")


def parse_isoformat_end_of_day_default(input_string: str) -> datetime:
    """helper function to provide to parse end dates"""
    return parse_isoformat(input_string, time_default="end")


def get_piped_args() -> str:
    """
    Attempt to read from standard input (stdin) and return the contents as a string.

    This function is designed to handle being executed in a variety of environments,
    including being called with 'nohup', in which case stdin may not be accessible.
    In such a scenario, it will log a warning and return an empty string.

    :return: A string containing the data read from stdin, or an empty string if stdin
             is not accessible (for example, when the script is executed with 'nohup').
    """
    try:
        return sys.stdin.read()
    except OSError:
        logger.warning(
            "Received OSError when trying to read stdin."
            "This is expected when executed with nohup."
        )
        return ""


def cli(command_line: Optional[Sequence[str]] = None) -> None:
    """eumdac entrypoint"""
    init_logger("INFO")

    # append piped args
    if not sys.stdin.isatty():
        pipe_args = get_piped_args()
        if pipe_args:
            sys.argv.extend(shlex.split(pipe_args))

    if command_line is not None:
        # when we are called directly (e.g. by tests) then mimic a call from
        # commandline by setting sys.argv accordingly
        sys.argv = ["eumdac"] + list(command_line)

    # main parser
    parser = argparse.ArgumentParser(description=__doc__, fromfile_prefix_chars="@")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase output verbosity (can be provided multiple times)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {eumdac.__version__}")
    parser.add_argument(
        "--set-credentials",
        nargs=2,
        action=SetCredentialsAction,
        help=argparse.SUPPRESS,
        metavar=("ConsumerKey", "ConsumerSecret"),
        dest="credentials",
    )
    parser.add_argument(
        "-y", "--yes", help="set any confirmation value to 'yes' automatically", action="store_true"
    )
    parser.add_argument(
        "--debug", help="show additional debugging info and traces for errors", action="store_true"
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--test", action="store_true", help=argparse.SUPPRESS)
    common_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase output verbosity (can be provided multiple times)",
    )
    common_parser.add_argument(
        "-y", "--yes", help="set any confirmation value to 'yes' automatically", action="store_true"
    )
    common_parser.add_argument(
        "--debug", help="show additional debugging info and traces for errors", action="store_true"
    )

    subparsers = parser.add_subparsers(dest="command")

    # credentials parser
    parser_credentials = subparsers.add_parser(
        "set-credentials",
        description="Set authentication parameters for the EUMETSAT APIs, see https://api.eumetsat.int/api-key",
        help=("permanently set consumer key and secret, " "see https://api.eumetsat.int/api-key"),
        parents=[common_parser],
    )
    parser_credentials.add_argument("ConsumerKey", help="consumer key")
    parser_credentials.add_argument("ConsumerSecret", help="consumer secret")
    parser_credentials.set_defaults(func=credentials)

    # token parser
    parser_token = subparsers.add_parser(
        "token",
        description="Generate an access token and exit",
        help="generate an access token",
        epilog="example: %(prog)s",
        parents=[common_parser],
    )
    parser_token.set_defaults(func=token)

    # describe parser
    parser_describe = subparsers.add_parser(
        "describe",
        description="Describe a collection or product, provide no arguments to list all collections",
        help="describe a collection or product",
        epilog="example: %(prog)s -c EO:EUM:DAT:MSG:HRSEVIRI",
        parents=[common_parser],
    )
    parser_describe.add_argument(
        "-f",
        "--filter",
        help="wildcard filter for collection identifier and name, e.g. *MSG*",
        dest="filter",
        type=str,
    )
    parser_describe.add_argument(
        "-c",
        "--collection",
        help="id of the collection to describe, e.g. EO:EUM:DAT:MSG:CLM",
        metavar="COLLECTION",
    )
    parser_describe.add_argument(
        "-p",
        "--product",
        help="id of the product to describe, e.g. MSG1-SEVI-MSGCLMK-0100-0100-20040129130000.000000000Z-NA",
        metavar="PRODUCT",
    )
    parser_describe.add_argument(
        "--flat",
        help="avoid tree view when showing product package contents",
        action="store_true",
    )
    parser_describe.set_defaults(func=describe)

    # search parser
    search_argument_parser = argparse.ArgumentParser(add_help=False)
    query_group = search_argument_parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument(
        "-q",
        "--query",
        nargs=1,
        help="opensearch query string, e.g. pi=EO:EUM:DAT:MSG:HRSEVIRI&dtstart=2023-06-21T12:27:42Z&dtend=2023-06-22T12:27:42Z",
    )
    query_group.add_argument("-c", "--collection", nargs="+", help="collection id")

    search_argument_parser.add_argument(
        "-s",
        "--start",
        type=parse_isoformat_beginning_of_day_default,
        help="sensing start date/time in UTC, e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
        dest="dtstart",
    )
    search_argument_parser.add_argument(
        "-e",
        "--end",
        type=parse_isoformat_end_of_day_default,
        help="sensing end date/time in UTC, e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
        dest="dtend",
    )
    search_argument_parser.add_argument(
        "--time-range",
        nargs=2,
        type=str,
        help="range of dates in UTC to search by sensing date/time",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_argument_parser.add_argument(
        "--publication-after",
        type=parse_isoformat_beginning_of_day_default,
        help="filter by publication date, products ingested after this UTC date e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_argument_parser.add_argument(
        "--publication-before",
        type=parse_isoformat_beginning_of_day_default,
        help="filter by publication date, products ingested before this UTC date e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_argument_parser.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("W", "S", "E", "N"),
        help="filter by bounding box, defined in EPSG:4326 decimal degrees, e.g. 51.28 51.69 0.51 0.33",
    )
    search_argument_parser.add_argument(
        "--geometry",
        help="filter by geometry, custom geometry in a EPSG:4326 decimal degrees, e.g. POLYGON ((10.09 56.09, 10.34 56.09, 10.34 56.19, 10.09 56.09))",
        dest="geo",
    )
    search_argument_parser.add_argument(
        "--cycle",
        help="filter by cycle number, must be a positive integer",
        dest="cycle",
        type=int,
    )
    search_argument_parser.add_argument(
        "--orbit",
        help="filter by orbit number, must be a positive integer",
        dest="orbit",
        type=int,
    )
    search_argument_parser.add_argument(
        "--relorbit",
        help="filter by relative orbit number, must be a positive integer",
        dest="relorbit",
        type=int,
    )
    search_argument_parser.add_argument(
        "--filename",
        help="wildcard filter by product identifier, e.g. *MSG*",
        dest="filename",
        type=str,
    )
    search_argument_parser.add_argument(
        "--timeliness",
        help="filter by timeliness",
        dest="timeliness",
        choices=["NT", "NR", "ST"],
    )
    search_argument_parser.add_argument(
        "--product-type",
        "--acronym",
        help="filter by product type/acronym, e.g. MSG15",
        dest="product_type",
        type=str,
    )
    search_argument_parser.add_argument(
        "--satellite", help="filter by satellite, e.g. MSG4", dest="sat"
    )
    search_argument_parser.add_argument(
        "--sort",
        choices=("ingestion", "sensing"),
        help="sort results by ingestion time or sensing time, default: sensing",
    )
    sorting_direction = search_argument_parser.add_mutually_exclusive_group(required=False)
    sorting_direction.add_argument("--asc", action="store_true", help="sort ascending")
    sorting_direction.add_argument("--desc", action="store_true", help="sort descending")
    search_argument_parser.add_argument(
        "--limit", type=int, help="max number of products to return"
    )
    parser_search = subparsers.add_parser(
        "search",
        description="Search for products",
        help="search for products",
        epilog="example: %(prog)s -c EO:EUM:DAT:MSG:CLM -s 2010-03-01 -e 2010-03-15T12:15",
        parents=[common_parser, search_argument_parser],
    )
    parser_search.add_argument(
        dest="print_help", nargs=0, action=HelpAction, help=argparse.SUPPRESS
    )
    parser_search.set_defaults(func=search)

    parser_download = subparsers.add_parser(
        "download",
        help="download products, with optional customisation",
        parents=[
            common_parser,
            search_argument_parser,
        ],  # this inherits collection lists
    )
    parser_download.add_argument(
        "-p", "--product", nargs="*", help="id of the product(s) to download"
    )
    parser_download.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        help="path to output directory, default: current directory",
        metavar="DIR",
        default=pathlib.Path.cwd(),
    )
    parser_download.add_argument(
        "-i",
        "--integrity",
        action="store_true",
        help="verify integrity of downloaded files through their md5, if available",
    )
    parser_download.add_argument(
        "--entry",
        nargs="+",
        help="shell-style wildcard pattern(s) to filter product files",
    )
    parser_download.add_argument(
        "--download-coverage",
        choices=["FD", "H1", "H2", "T1", "T2", "T3", "Q1", "Q2", "Q3", "Q4"],
        help="download only the area matching the provided coverage (only for specific missions)",
    )
    parser_download.add_argument(
        "--tailor",
        help="chain file or YAML string for customising the data",
        metavar="CHAIN",
    )
    parser_download.add_argument(
        "--chain",
        help="chain file or YAML string for customising the data",
        metavar="CHAIN",
    )
    parser_download.add_argument(
        "--local-tailor",
        help="id of the instance to use for customisating the data",
        metavar="ID",
    )
    dir_group = parser_download.add_mutually_exclusive_group()
    dir_group.add_argument(
        "--onedir", action="store_true", help="avoid creating a subdirectory for each product"
    )
    dir_group.add_argument(
        "--dirs",
        help="download each product into its own individual directory",
        action="store_true",
    )
    parser_download.add_argument(
        "-k",
        "--keep-order",
        action="store_true",
        help="keep order file after finishing successfully",
    )
    parser_download.add_argument(
        "--no-warning-logs", help="don't show logs when jobs fail", action="store_true"
    )
    parser_download.add_argument(
        "--no-progress-bars", help="don't show download progress bars", action="store_true"
    )
    parser_download.add_argument(
        dest="print_help", nargs=0, action=HelpAction, help=argparse.SUPPRESS
    )
    parser_download.set_defaults(func=download)

    # tailor parser
    # tailor parser common arguments
    tailor_common_parser = argparse.ArgumentParser(add_help=False)
    tailor_common_parser.add_argument(
        "--local-tailor",
        help="id of the instance to use for customisating the data",
        metavar="ID",
    )

    parser_tailor = subparsers.add_parser(
        "tailor",
        description="Manage Data Tailor customisations",
        help="manage Data Tailor resources",
        parents=[common_parser],
    )
    parser_tailor.add_argument(
        dest="print_help", nargs=0, action=HelpAction, help=argparse.SUPPRESS
    )
    tailor_subparsers = parser_tailor.add_subparsers(dest="tailor-command")

    tailor_post_parser = tailor_subparsers.add_parser(
        "post",
        description="Post individual customisation jobs",
        help="post a new customisation job",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_post_parser.add_argument("-c", "--collection", help="collection id")
    tailor_post_parser.add_argument(
        "-p", "--product", nargs="+", help="id of the product(s) to customise"
    )
    tailor_post_parser.add_argument(
        "--chain",
        help="chain file or YAML string for customising the data",
        metavar="CHAIN",
    )
    tailor_post_parser.set_defaults(func=tailor_post_job)

    tailor_list_parser = tailor_subparsers.add_parser(
        "list",
        description="List customisation jobs",
        help="list customisation jobs",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_list_parser.set_defaults(func=tailor_list_customisations)

    tailor_status_parser = tailor_subparsers.add_parser(
        "status",
        description="Check the status of one (or more) customisations",
        help="check the status of customisations",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_status_parser.add_argument("job_ids", metavar="Customisation ID", type=str, nargs="+")
    tailor_status_parser.set_defaults(func=tailor_show_status)

    tailor_log_parser = tailor_subparsers.add_parser(
        "log",
        description="Get the log of a customisation",
        help="get the log of a customisation",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_log_parser.add_argument(
        "job_id", metavar="Customisation ID", type=str, help="Customisation ID"
    )
    tailor_log_parser.set_defaults(func=tailor_get_log)

    tailor_quota_parser = tailor_subparsers.add_parser(
        "quota",
        description="Show user workspace usage quota. Verbose mode (-v) shows more details",
        help="show user workspace usage quota",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_quota_parser.set_defaults(func=tailor_quota)

    tailor_delete_parser = tailor_subparsers.add_parser(
        "delete",
        description="Delete finished customisations",
        help="delete customisations",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_delete_parser.add_argument("job_ids", metavar="Customisation ID", type=str, nargs="+")
    tailor_delete_parser.set_defaults(func=tailor_delete_jobs)

    tailor_cancel_parser = tailor_subparsers.add_parser(
        "cancel",
        description="Cancel QUEUED, RUNNING or INACTIVE customisations",
        help="cancel running customisations",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_cancel_parser.add_argument("job_ids", metavar="Customisation ID", type=str, nargs="+")
    tailor_cancel_parser.set_defaults(func=tailor_cancel_jobs)

    tailor_clean_parser = tailor_subparsers.add_parser(
        "clean",
        description="Clean up customisations in any state (cancelling them if needed)",
        help="clean up customisations in any state",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_clean_parser.add_argument("job_ids", metavar="Customisation ID", type=str, nargs="*")
    tailor_clean_parser.add_argument("--all", help="Clean all customisations", action="store_true")
    tailor_clean_parser.set_defaults(func=tailor_clear_jobs)

    tailor_download_parser = tailor_subparsers.add_parser(
        "download",
        description="Download the output of finished customisations",
        help="download the output of finished customisations",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_download_parser.add_argument(
        "job_id", metavar="Customisation ID", type=str, help="Customisation ID"
    )
    tailor_download_parser.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        help="path to output directory, default: current directory",
        metavar="DIR",
        default=pathlib.Path.cwd(),
    )
    tailor_download_parser.set_defaults(func=tailor_download)

    # Local Data Tailor instances parser
    parser_local_tailor = subparsers.add_parser(
        "local-tailor",
        description="Manage local Data Tailor instances",
        help="manage local Data Tailor instances",
        parents=[common_parser],
    )
    parser_local_tailor.add_argument(
        dest="print_help", nargs=0, action=HelpAction, help=argparse.SUPPRESS
    )
    local_tailor_subparsers = parser_local_tailor.add_subparsers(dest="local_tailor_command")

    local_tailor_list_parser = local_tailor_subparsers.add_parser(
        "instances",
        help="list configured instances",
        description="List configured local Data Tailor instances",
        parents=[common_parser],
    )
    local_tailor_list_parser.set_defaults(func=local_tailor)

    local_tailor_show_parser = local_tailor_subparsers.add_parser(
        "show",
        help="show details of an instance",
        description="Show details of local Data Tailor instances",
        parents=[common_parser],
    )
    local_tailor_show_parser.add_argument(
        "localtailor_id",
        help="id of the local instance, e.g. my-local-tailor",
        metavar="ID",
        nargs=1,
    )
    local_tailor_show_parser.set_defaults(func=local_tailor)

    local_tailor_set_parser = local_tailor_subparsers.add_parser(
        "set",
        help="configure a local instance",
        description=f"Configure a local Data Tailor instance",
        parents=[common_parser],
    )
    local_tailor_set_parser.add_argument(
        "localtailor_id",
        help="id for the local instance, e.g. my-local-tailor",
        metavar="ID",
        nargs=1,
    )
    local_tailor_set_parser.add_argument(
        "localtailor_url",
        help="base URL of the local instance, e.g. http://localhost:40000/",
        metavar="URL",
        nargs=1,
    )
    local_tailor_set_parser.set_defaults(func=local_tailor)

    local_tailor_remove_parser = local_tailor_subparsers.add_parser(
        "remove",
        help="remove a configured instance",
        description="Remove a configured local instance",
        parents=[common_parser],
    )
    local_tailor_remove_parser.add_argument(
        "localtailor_id",
        help="id of the local instance, e.g. my-local-tailor",
        metavar="ID",
        nargs=1,
    )
    local_tailor_remove_parser.set_defaults(func=local_tailor)

    #  Order parser
    parser_order = subparsers.add_parser(
        "order",
        description="Manage eumdac orders",
        help="manage orders",
        parents=[common_parser],
    )
    parser_order.add_argument(dest="print_help", nargs=0, action=HelpAction, help=argparse.SUPPRESS)
    order_subparsers = parser_order.add_subparsers(dest="order_command")
    order_parsers = {}
    order_parsers["list"] = order_subparsers.add_parser(
        "list",
        description="List eumdac orders",
        help="list orders",
        parents=[common_parser],
    )
    order_parsers["list"].set_defaults(func=order)
    for action in ["status", "resume", "restart", "delete"]:
        subparser = order_subparsers.add_parser(
            action,
            description=f"{action.capitalize()} eumdac orders",
            help=f"{action} orders",
            parents=[common_parser],
        )
        if action in ["resume", "restart"]:
            subparser.add_argument(
                "-i",
                "--integrity",
                action="store_true",
                help="verify integrity of downloaded files through their md5, if available",
            )
            subparser.add_argument(
                "--local-tailor",
                help="id of the instance to use for customisating the data",
                metavar="ID",
            )
            subparser.add_argument(
                "-k",
                "--keep-order",
                action="store_true",
                help="keep order file after finishing successfully",
            )
        subparser.add_argument(
            "order_id", help="order id", metavar="ID", nargs="?", default="latest"
        )
        if action == "delete":
            subparser.add_argument("--all", help="delete all orders", action="store_true")
        subparser.set_defaults(func=order)
        order_parsers[action] = subparser

    args = parser.parse_args(command_line)
    if hasattr(args, "time_range"):
        args.dtstart, args.dtend = _parse_timerange(args)
        del args.time_range

    # initialize logging
    try:
        progress_bars = not args.no_progress_bars
    except AttributeError:
        progress_bars = True
    if args.debug:
        init_logger("DEBUG", progress_bars)
    elif args.verbose > 1:
        init_logger("VERBOSE", progress_bars)
    else:
        init_logger("INFO", progress_bars)

    if args.command:
        if args.test:
            return args.func(args)

        try:
            args.func(args)
        except KeyboardInterrupt:
            # Ignoring KeyboardInterrupts to allow for clean CTRL+C-ing
            pass
        except Exception as error:
            log_error(error)
            if args.debug:
                raise
            sys.exit(1)
    else:
        parser.print_help()


def log_error(error: Exception) -> None:
    logger.error(str(error))
    if isinstance(error, EumdacError) and error.extra_info:  # type:ignore
        extra_info: Dict[str, Any] = error.extra_info  # type: ignore

        extra_msg: str = ""
        if "text" in extra_info:
            extra_msg += f"{extra_info['text']}, "
        if "title" in extra_info:
            extra_msg += f"{extra_info['title']} "
        if "description" in extra_info:
            extra_msg += f"{extra_info['description']} "
        if extra_msg:
            # Add the status code only if there's more info
            if "status" in extra_info:
                extra_msg = f"{extra_info['status']} - {extra_msg}"
            logger.error(extra_msg)

        if "exceptions" in extra_info:
            for problem in extra_info["exceptions"]:
                detail_msg: str = f"{extra_info['status']} - {problem['exceptionText']}"
                if not ("NoApplicableCode" in problem["exceptionCode"]):
                    detail_msg += f" - Type: {problem['exceptionCode']}"
                logger.error(detail_msg)


class CredentialsFileNotFoundError(EumdacError):
    """Error that will be raised when no credentials file is found"""
