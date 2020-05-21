from metaloader.stanzahandlers.dict import DictStanzaHandler


class ObjectsStanzaHandler(DictStanzaHandler, register="objects"):
    def _initialise(self):
        return {
            "prefixlists": {},
            "appdefs": {
                "apps": {},
                "appgroups": {}
            }
        }

    def _merge(self, stanza_data: dict, new_data: dict):
        if "prefixlists" in new_data:
            stanza_data["prefixlists"].update(new_data["prefixlists"])
        if "appdefs" in new_data:
            appdefs = new_data["objects"]
            for key in ("apps", "appdefs"):
                if key in appdefs:
                    stanza_data["appdefs"][key].update(appdefs[key])
