import configparser


def createConfig(path_new):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "token", "5975391066:AAEHxpuSeVYz4fidfGbV61zuKN4zOrxGvDY")
    config.set("Settings", "sleep_mode", "False")

    with open(path_new, "w") as config_file:
        config.write(config_file)


if __name__ == "__main__":
    path = "utils/settings.ini"
    createConfig(path)
