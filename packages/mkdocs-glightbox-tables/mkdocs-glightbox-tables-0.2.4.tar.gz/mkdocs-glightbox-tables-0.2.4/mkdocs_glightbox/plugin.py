import json
import logging
import os
import pathlib
from xml.dom.minidom import Element
from copy import deepcopy, copy

from bs4 import BeautifulSoup
from mkdocs import utils
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

log = logging.getLogger(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))


def get_tables(html):
    return BeautifulSoup(html, "html.parser").find_all("table")


def get_pruned_tables(html):
    tables = []
    n_tables = len(get_tables(html))
    for i in range(n_tables):
        table = get_tables(html)[i]  # TODO : find a more elegant solution ..
        tables.append(prune(table))
    return tables


def prune(elem):
    pruned = elem
    del pruned["class"]  # For uniform styling
    parent = pruned.parent

    while parent is not None:  # and "html" not in parent.name:
        print("CLASS: ",parent.get("class"))
        if (parent.get("class", None) is None) or ("tabbed" in "".join(parent.get("class", ""))) :
            parent = parent.parent
            continue
            
        parent["style"] = "text-align: center"
        # Adding an "open" attribute for collapsible sections
        parent["open"] = ""
        parent.clear()
        parent.append(pruned)
        pruned = parent
        parent = parent.parent

    return pruned

def limit_number_lines(table, max_n_lines, skip_class=[]):
    if set(skip_class) & (set(table.get("class", [])) | set(table.parent.get("class", []))):
        return table
    [row.extract() for i, row in enumerate(table.find_all("tr")) if i > max_n_lines]
    last_row = list(table.find_all("tr"))[-1]
    for cell in last_row.find_all("td"):
        cell.string = "..."
    return table


class LightboxPlugin(BasePlugin):
    """Add lightbox to MkDocs"""

    config_scheme = (
        ("touchNavigation", config_options.Type(bool, default=True)),
        ("loop", config_options.Type(bool, default=False)),
        ("effect", config_options.Choice(("zoom", "fade", "none"), default="zoom")),
        ("width", config_options.Type(str, default="100%")),
        ("height", config_options.Type(str, default="1000px")),
        ("zoomable", config_options.Type(bool, default=True)),
        ("draggable", config_options.Type(bool, default=True)),
        ("max_preview_lines", config_options.Type(int, default=5)),
        ("skip_classes", config_options.Type(list, default=[])),
    )

    def on_post_page(self, output, page, config, **kwargs):
        """Add css link tag, javascript script tag, and javascript code to initialize GLightbox"""

        if "glightbox" in page.meta and page.meta.get("glightbox", True) is False:
            return output

        soup = BeautifulSoup(output, "html.parser")

        if soup.head:
            css_link = soup.new_tag("link")
            css_link.attrs["href"] = utils.get_relative_url(
                utils.normalize_url("assets/stylesheets/glightbox.min.css"), page.url
            )
            css_link.attrs["rel"] = "stylesheet"
            soup.head.append(css_link)

            css_patch = soup.new_tag("style")
            css_patch.string = (
                "html.glightbox-open { overflow: initial; height: 100%; }"
            )
            soup.head.append(css_patch)

            js_script = soup.new_tag("script")
            js_script.attrs["src"] = utils.get_relative_url(
                utils.normalize_url("assets/javascripts/glightbox.min.js"), page.url
            )
            soup.head.append(js_script)

            js_code = soup.new_tag("script")
            plugin_config = dict(self.config)
            lb_config = {
                k: plugin_config[k]
                for k in [
                    "touchNavigation",
                    "loop",
                    "width",
                    "height",
                    "zoomable",
                    "draggable",
                ]
            }
            lb_config["openEffect"] = plugin_config.get("effect", "zoom")
            lb_config["closeEffect"] = plugin_config.get("effect", "zoom")
            js_code.string = f"const lightbox = GLightbox({json.dumps(lb_config)});"
            if config["theme"].name == "material" or "navigation.instant" in config[
                "theme"
            ]._vars.get("features", []):
                # support compatible with mkdocs-material Instant loading feature
                js_code.string = "document$.subscribe(() => {" + js_code.string + "})"
            soup.body.append(js_code)

        # Getting pruned tables
        head = BeautifulSoup(output, "html.parser").head
        tables = get_pruned_tables(output)
        output_dir = config["site_dir"] / pathlib.Path(page.url)

        skip_class = ["off-glb"] + self.config["skip_classes"]

        for i, table in enumerate(tables):
            output_file = output_dir / f"{i}.html"
            output_file.parent.mkdir(exist_ok=True, parents=True)
            output_file.write_text(str(head) + "\n" + str(table))

        # Adding GLightBox link + limiting number of lines
        tables = soup.find_all("table")
        tables = [
            limit_number_lines(table, plugin_config["max_preview_lines"], skip_class)
            for table in tables
        ]
        for i, table in enumerate(tables):
            if set(skip_class) & (set(table.get("class", [])) | set(table.parent.get("class", []))):
                continue
            output_file = f"{i}.html"
            table["title"] = "Click to view the full table"

            a = soup.new_tag("a")
            a["class"] = "glightbox"
            a["href"] = output_file
            table.wrap(a)

        return str(soup)

    def on_page_content(self, html, page, config, **kwargs):
        """Wrap img tag with archive tag with glightbox class and attributes from config"""
        # skip page with meta glightbox is false
        if "glightbox" in page.meta and page.meta.get("glightbox", True) is False:
            return html
        # skip emoji img with index as class name from pymdownx.emoji https://facelessuser.github.io/pymdown-extensions/extensions/emoji/
        skip_class = ["emojione", "twemoji", "gemoji"]
        # skip image with off-glb class
        skip_class += ["off-glb"] + self.config["skip_classes"]
        soup = BeautifulSoup(html, "html.parser")
        imgs = soup.find_all(["img", "iframe"])
        for img in imgs:
            if set(skip_class) & set(img.get("class", [])):
                continue
            a = soup.new_tag("a")
            a["class"] = "glightbox"
            a["href"] = img.get("src", "")
            img.wrap(a)

        return str(soup)

    def on_post_build(self, config, **kwargs):
        """Copy glightbox"s css and js files to assets directory"""

        output_base_path = os.path.join(config["site_dir"], "assets")
        css_path = os.path.join(output_base_path, "stylesheets")
        utils.copy_file(
            os.path.join(base_path, "glightbox", "glightbox.min.css"),
            os.path.join(css_path, "glightbox.min.css"),
        )
        js_path = os.path.join(output_base_path, "javascripts")
        utils.copy_file(
            os.path.join(base_path, "glightbox", "glightbox.min.js"),
            os.path.join(js_path, "glightbox.min.js"),
        )
