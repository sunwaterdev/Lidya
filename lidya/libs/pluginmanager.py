"""Lidya plugin manager (by SunWAter_ )"""
import os
import json


class PluginManager:
    """Global plugin manager"""
    def execute_plugin_action(self, action_name, args=None):
        """Execute action from LLM"""
        plugin_name, action = action_name.split(".")
        plugin_module = __import__(f"plugins.{plugin_name}", fromlist=[""])
        main_class = getattr(plugin_module, "Main")()

        if hasattr(main_class, action):
            if args:
                result = getattr(main_class, action)(**args)
            else:
                result = getattr(main_class, action)()
            return result
        print(f"The action'{action}' of plugin '{plugin_name}' doesn't exsists.")
        return None

    def process_actions(self, actions):
        """Lydia process actions from LLM"""
        results = {}

        for action in actions:
            action_name = action["name"]

            if action["args"] == {}:
                result = self.execute_plugin_action(action_name)
            else:
                mapping = {action['name']: action['value']}

                result = self.execute_plugin_action(action_name, args=mapping)

            if result is not None:
                results[action_name] = result

        return results

    def load_plugins(self):
        """Lidya load plugins."""
        plugin_loc = "./plugins"
        plugins = os.listdir(plugin_loc)

        plugin_manager_json = []
        plugin_json_conf = None

        for plugin in plugins:
            try:
                with open("./plugins/" + plugin + "/plugin.json", "r",
                          encoding="utf-8") as plugin_conf:
                    plugin_json_conf = json.load(plugin_conf)
            except FileNotFoundError:
                print(f"The {plugin} plugin was not loaded correctly: FileNotFoundError.")

            plugin_manager_json.append(plugin_json_conf)

        return plugin_manager_json
