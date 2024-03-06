# Copyright Capgemini Engineering B.V.

"""Publish Pages."""
import os
from os import getcwd, path
from shutil import copytree, copyfile

import yaml
from loguru import logger
import i18n

from jinja2 import Environment, FileSystemLoader, select_autoescape

from acidcli.tasks.executable import Executable
from acidcli.facility.decorators import print_job_info, function_debug
from acidcli.exceptions import CLIError


# pylint: disable=too-few-public-methods
class Pages(Executable):
    """Publish pages."""

    def __init__(self):
        """Init."""
        self.__job = None

    @print_job_info
    def execute(self, job):
        """Publish pages."""
        self.__job = job
        self._required_parameters_available(self.__job, ["config", "output"])

        config_file = self._parameter_value(self.__job, "config")
        output_directory = self._parameter_value(self.__job, "output")
        config = self.__get_config(config_file)

        base_path = path.abspath(path.join(path.dirname(__file__), "..", "..", "..", "defaults", "pages"))
        template_path = path.join(base_path, "templates")
        template_page_path = path.join(template_path, "page.jinja")
        template_css_path = path.join(template_path, "capgemini.jinja")

        self.__prepare_dashboard_page(base_path, output_directory)
        self.__copy_directories(config, config_file, output_directory)

        template_page_str = self.__read_template(template_page_path)
        template_css_str = self.__read_template(template_css_path)

        self.__create_dashboard_page(config, base_path, output_directory, template_page_str, template_css_str)

        pages_url = os.environ.get("CI_PAGES_URL")
        if pages_url is not None:
            logger.info(
                i18n.t(
                    "acidcli.publish_pages.url_found",
                    url=pages_url,
                )
            )

    @staticmethod
    @function_debug
    def __get_config(config_file):
        """Return config."""
        try:
            with open(path.join(getcwd(), config_file), "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except OSError as error:
            raise CLIError(
                i18n.t(
                    "acidcli.file_or_folder_not_found",
                    filename=config_file,
                ),
            ) from error
        except yaml.YAMLError as error:
            raise CLIError(
                i18n.t(
                    "acidcli.invalid_configuration",
                    filename=config_file,
                ),
            ) from error

    @function_debug
    def __copy_directories(self, config, config_file, output_directory):
        """Copy directories."""
        logger.debug(config)

        try:
            for page in config["pages"]:
                try:
                    copytree(page["input"], path.join(output_directory, page["output"]))
                except FileNotFoundError as error:
                    if page["mandatory"]:
                        raise CLIError(i18n.t("acidcli.file_or_folder_not_found", filename=page["input"])) from error

                    logger.warning(
                        i18n.t("acidcli.publish_pages.warning_file_or_folder_not_found", filename=page["input"])
                    )
                self.__copy_icon(output_directory, page)

            if "bookmarks" in config.keys():
                for bookmark in config["bookmarks"]:
                    self.__copy_icon(output_directory, bookmark)

            self.__copy_named_element("favicon", config, output_directory)
            self.__copy_named_element("logo", config, output_directory)

        except (TypeError, KeyError) as error:
            raise CLIError(
                i18n.t(
                    "acidcli.invalid_configuration",
                    filename=config_file,
                ),
            ) from error

    @staticmethod
    @function_debug
    def __copy_icon(output_directory, element):
        """__copy_icon.

        Copy given icon to output directory,
           if icon is located in the project repo then that one is copied
           if icon is located in the build-in repo then that one is copied

        param output_directory: location of output directory
        param element: element
        """
        default_icon_repo = path.join(path.dirname(__file__), "..", "..", "..", "defaults", "pages", "static")

        if "icon" in element:
            basename = path.basename(element["icon"])
            default_icon = path.join(default_icon_repo, element["icon"])
            # peek if this resource is local
            src = None
            if path.exists(element["icon"]):
                src = element["icon"]
            elif path.exists(default_icon):
                src = default_icon

            try:
                copyfile(src, path.join(output_directory, "static", basename))
            except FileNotFoundError as error:
                raise CLIError(i18n.t("acidcli.file_or_folder_not_found", filename=element["icon"])) from error

    @staticmethod
    @function_debug
    def __copy_named_element(element, config, output_directory):
        """__copy_named_element.

        param element: the to copied element in the config
        param config: the configuration
        param output_directory: the destiny folder
        """
        try:
            if element in config:
                copyfile((config[element]), path.join(output_directory, "static", path.basename(config[element])))
        except FileNotFoundError as error:
            raise CLIError(i18n.t("acidcli.file_or_folder_not_found", filename=config[element])) from error

    @staticmethod
    @function_debug
    def __prepare_dashboard_page(base_path, output_directory):
        """Prepare dashboard page."""
        static_path = path.join(base_path, "static")

        try:
            copytree(static_path, path.join(output_directory, "static"))
        except FileNotFoundError:
            logger.warning(i18n.t("acidcli.publish_pages.warning_file_or_folder_not_found", filename=static_path))

    @function_debug
    def __read_template(self, template_file__path):
        """Read template."""
        return self.__try_file_read(template_file__path)

    @staticmethod
    @function_debug
    def __try_file_read(file_path):
        """__try_file_read.

        param file_path:
        return file_str: file content
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_str = file.read()
        except OSError as error:
            raise CLIError(
                i18n.t(
                    "acidcli.file_or_folder_not_found",
                    filename=file_path,
                ),
            ) from error
        return file_str

    @function_debug
    def __create_dashboard_page(self, config, base_path, output_directory, template_page_str, template_css_str):
        """Generate and write dashboard."""
        template_path = path.join(base_path, "templates")
        template_page_path = path.join(template_path, "page.jinja")
        output_page = path.join(output_directory, "index.html")
        template_css_path = path.join(template_path, "capgemini.jinja")
        output_css = path.join(output_directory, "static", "capgemini.css")

        j2_page_template = Environment(
            loader=FileSystemLoader(template_path), autoescape=select_autoescape()
        ).from_string(template_page_str)
        content = j2_page_template.render(self.__parse_configuration(config))

        j2_css_template = Environment(
            loader=FileSystemLoader(template_path), autoescape=select_autoescape()
        ).from_string(template_css_str)

        self.__try_write_file(content, output_page, template_page_path)

        css_content = j2_css_template.render(self.__parse_css(config))

        self.__try_write_file(css_content, output_css, template_css_path)

    @staticmethod
    def __try_write_file(content, output_filename, template_file_path):
        """__try_write_file.

        param content:
        param output_filename:
        param template_file_path:
        """
        try:
            with open(output_filename, "w+", encoding="utf-8") as output_file:
                output_file.write(content)
        except OSError as error:
            raise CLIError(
                i18n.t(
                    "acidcli.file_or_folder_not_found",
                    filename=template_file_path,
                ),
            ) from error

    @staticmethod
    def __parse_css(config):
        """__parse_css.

        Generate a dict form yaml content

        param config: input configuration dict from yaml
        return configuration: dict readable for jinja/html
        """
        configuration = {}

        if "primary_color" in config:
            configuration["primary_color"] = path.basename(str(config["primary_color"]))
        if "secondary_color" in config:
            configuration["secondary_color"] = path.basename(str(config["secondary_color"]))

        return configuration

    @function_debug
    def __parse_configuration(self, config):
        """__parse_configuration.

        Generate a html dict form yaml content

        param config: input configuration dict from yaml
        return configuration: dict readable for jinja/html
        """
        tiles_configuration = []
        configuration = {}

        if "pages" in config:
            for page in config["pages"]:
                page_data = self.__parse_page_data(page)

                tiles_configuration.append(page_data)

        if "bookmarks" in config:
            for bookmark in config["bookmarks"]:
                bookmark_data = self.__parse_bookmark_data(bookmark)

                tiles_configuration.append(bookmark_data)

        configuration["pages_configuration"] = tiles_configuration

        self.__parse_main_part(config, configuration)

        return configuration

    @staticmethod
    @function_debug
    def __parse_main_part(config, configuration):
        """__parse_main_part.

        param config: input configuration dict from yaml
        param configuration: output configuration to jinja/html
        """
        if "title" in config:
            configuration["title"] = config["title"]
        if "support_email" in config:
            configuration["support_email"] = config["support_email"]
        if "powered_by" in config:
            configuration["powered_by"] = config["powered_by"]
        if "logo" in config:
            configuration["logo"] = path.basename(config["logo"])
        if "favicon" in config:
            configuration["favicon"] = path.basename(config["favicon"])

    @staticmethod
    @function_debug
    def __parse_bookmark_data(bookmark):
        """__parse_bookmark_data.

        param bookmark:
        return page_data: configuration
        """
        bookmark_data = {"title": bookmark["title"], "link": bookmark["url"], "exists": True}
        if "icon" in bookmark:
            bookmark_data["icon"] = path.basename(bookmark["icon"])
        return bookmark_data

    @function_debug
    def __parse_page_data(self, page):
        """__parse_page_data.

        param page:
        return page_data: configuration
        """
        page_data = {
            "title": page["title"],
            "link": page["output"],
            "exists": path.isdir(path.join(self._parameter_value(self.__job, "output"), page["output"])),
        }
        if "icon" in page:
            page_data["icon"] = path.basename(page["icon"])
        return page_data


# pylint: enable=too-few-public-methods
