from scrapy.http import HtmlResponse


class FormExtractor:
    def __init__(self) -> None:
        pass

    def extract_forms(self, response: HtmlResponse):
        forms = []
        for form_element in response.css("form"):
            form = {
                "url": form_element.attrib.get("action"),
                "method": form_element.attrib.get("method"),
                "inputs": [],
            }
            for input in form_element.css("input"):
                form["inputs"].append(
                    {
                        "name": input.attrib.get("name"),
                        "type": input.attrib.get("type", "text"),
                    }
                )

            forms.append(form)

        return forms
