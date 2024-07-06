import os
import json
import ipdb


class PluginManager:
    def execute_plugin_action(self, action_name, args=None):
        plugin_name, action = action_name.split('.')
        plugin_module = __import__(f"plugins.{plugin_name}", fromlist=[''])
        main_class = getattr(plugin_module, 'Main')()

        if hasattr(main_class, action):
            if args:
                result = getattr(main_class, action)(**args)
            else:
                result = getattr(main_class, action)()
            return result
        else:
            print(f"The action'{action}' of plugin '{plugin_name}' doesn't exsists.")

        
    
    def process_actions(self, actions):
        results = {}

        for action in actions:
            action_name = action['name']

            if action['args'] == {}:
                result = self.execute_plugin_action(action_name)
            else:
                print(action['args'])
                mapping = {element['name']: element['value'] for element in action['args']}
                print(mapping)
                result = self.execute_plugin_action(action_name, args=mapping)

            if result is not None:
                results[action_name] = result

        return results

    def load_plugins(self):
        plugin_loc = "./plugins"
        plugins = os.listdir(plugin_loc)

        plugin_manager_json = []
        plugin_json_conf = None

        for plugin in plugins:
            try:
                plugin_conf = open('./plugins/'+plugin+'/plugin.json', 'r')
                plugin_json_conf = json.load(plugin_conf)
            except Exception as e:
                print(f'The {plugin} plugin was not loaded correctly: {e}')
        
            plugin_manager_json.append(plugin_json_conf)

        print(plugin_manager_json)

        return plugin_manager_json