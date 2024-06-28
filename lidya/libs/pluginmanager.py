# Fonction pour exécuter une action de plugin

class PluginManager:
    def execute_plugin_action(self, action_name, arguments=None):
        try:
            # Séparation du nom du plugin et de l'action
            plugin_name, action = action_name.split('.')
        
            # Importation du module du plugin et récupération de la classe Main
            plugin_module = __import__(f"plugins.{plugin_name}", fromlist=[''])
            main_class = getattr(plugin_module, 'Main')()
        
            # Vérification de la présence de la méthode d'action
            if hasattr(main_class, action):
                # Exécution de la fonction d'action avec ou sans arguments
                print(arguments)
                if arguments:
                    result = getattr(main_class, action)(**arguments)
                else:
                    result = getattr(main_class, action)()
                return result
            else:
                print(f"La fonction d'action '{action}' du plugin '{plugin_name}' est introuvable.")
        except ImportError:
            print(f"Le plugin '{plugin_name}' n'a pas pu être chargé.")
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'exécution du plugin '{plugin_name}' pour l'action '{action}': {e}")
            return None
        
    
    def process_actions(self, actions):
        results = {}

        # Parcours de chaque action de plugin
        for action in actions:
            action_name = action['name']

            if action['args'] == {}:
                result = self.execute_plugin_action(action_name)
            else:
                print(action['args'])
                mapping = {element['name']: element['value'] for element in action['args']}
                print(mapping)
                result = self.execute_plugin_action(action_name, arguments=mapping)

            if result is not None:
                results[action_name] = result

        return results

    
