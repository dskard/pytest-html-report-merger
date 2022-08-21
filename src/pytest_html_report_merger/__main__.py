import argparse
import logging
import bs4
import copy
import os
import re


log = logging.getLogger(__name__)


def parse_arguments():
    command_parser = argparse.ArgumentParser()

    command_parser.add_argument(
        "--out",
        help="name of the output html report",
        action="store",
        dest="out",
        default="merged.html",
        type=str,
    )

    command_parser.add_argument(
        "--verbose",
        "-v",
        help="level of logging verbosity",
        default=3,
        action="count",
    )

    command_parser.add_argument(
        "html_files",
        help="html files generated by pytest-html",
        action="store",
        nargs="*",
        type=str,
    )

    # parse options
    options = command_parser.parse_args()

    return options


class PytestHTMLReportMerger:
    def __init__(self):
        self.base = None

    def process_report(self, report_path):

        # open the first html file
        html_doc = ""
        with open(report_path, "r") as f:
            html_doc = f.read()
        soup = bs4.BeautifulSoup(html_doc, features="html.parser")

        report_name = os.path.basename(report_path)

        # update the base report
        if self.base is None:

            # this is the first report
            self.base = copy.copy(soup)

            # add a sortable column for report name
            col_report = self.base.new_tag(
                "th", attrs={"class": "sortable", "col": "report"}
            )
            col_report.string = "Report"

            results_table_head = self.base.select(
                "#results-table-head tr:nth-child(1)"
            )[0]
            results_table_head.append(col_report)

            # add the report column to each result table item
            # expand the details row colspan to accomodate the new column
            for ele in self.base.select(".results-table-row"):
                # create the new column
                col_report = self.base.new_tag("td", attrs={"class": "col-report"})
                col_report.string = report_name
                # add it to the first row
                ele_row_1 = ele.select("tr:nth-child(1)")[0]
                ele_row_1.append(col_report)
                # adjust the second row colspan
                ele_row_2 = ele.select("tr:nth-child(2) .extra")[0]
                ele_row_2["colspan"] = str(int(ele_row_2["colspan"]) + 1)

            return

        # parse the summary

        # parse the number of tests and timings
        base_element = self.base.find("p", string=re.compile("tests ran in"))
        matches = re.search(r"(\d+) tests ran in (\d+(\.\d+)?)", base_element.string)
        base_total_tests = int(matches.groups()[0])
        base_total_time = float(matches.groups()[1])

        soup_element = soup.find("p", string=re.compile("tests ran in"))
        matches = re.search(r"(\d+) tests ran in (\d+(\.\d+)?)", soup_element.string)
        soup_total_tests = int(matches.groups()[0])
        soup_total_time = float(matches.groups()[1])

        total_tests = base_total_tests + soup_total_tests
        total_time = base_total_time + soup_total_time
        base_element.string = f"{total_tests} tests ran in {total_time} seconds."

        # parse the counts

        for key in [
            "passed",
            "skipped",
            "failed",
            "error",
            "xfailed",
            "xpassed",
            "rerun",
        ]:
            # find the base's value for the key
            base_elements = self.base.select(f"span.{key}")
            matches = re.search("(\d+)", base_elements[0].string)
            base_value = int(matches.groups()[0])

            # find the soup's value for the key
            soup_elements = soup.select(f"span.{key}")
            matches = re.search("(\d+)", soup_elements[0].string)
            soup_value = int(matches.groups()[0])

            # save the updated count to the base
            base_elements[0].string = re.sub(
                r"\d+", str(base_value + soup_value), base_elements[0].string
            )

            # remove the base's disabled filter
            if base_value == 0 and soup_value != 0:
                ele = self.base.select(f"[data-test-result='{key}']")[0]
                del ele["disabled"]

        # update the base report's results table
        base_results_table = self.base.select("#results-table")[0]
        soup_tbodys = soup.select("#results-table tbody")

        for ele in soup_tbodys:
            ele_copy = copy.copy(ele)

            # add the report column
            ele_copy_tr = ele_copy.select("tr:nth-child(1)")[0]
            col_report = self.base.new_tag("td", attrs={"class": "col-report"})
            col_report.string = report_name
            ele_copy_tr.append(col_report)

            # adjust the second row colspan
            ele_row_2 = ele_copy.select("tr:nth-child(2) .extra")[0]
            ele_row_2["colspan"] = str(int(ele_row_2["colspan"]) + 1)

            # add the copied element to the base
            base_results_table.append(ele_copy)

    def write_report(self, report_path):
        # update report header
        report_header = os.path.basename(report_path)
        self.base.h1.string = report_header

        # write to file
        with open(report_path, "w") as f:
            f.write(str(self.base))


def main(arguments):

    # create a report merger object
    report_merger = PytestHTMLReportMerger()

    # process each of the input files
    for infile in arguments.html_files:
        report_merger.process_report(infile)

    # write the merged report to disk
    report_merger.write_report(arguments.out)


def cli():

    arguments = parse_arguments()

    logging.basicConfig(level=int((6 - arguments.verbose) * 10))

    log.debug(f"opts = {arguments}")

    main(arguments)

    log.debug("exiting")
