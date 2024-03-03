"""This module contains the PalWorldSettings class."""


class PalWorldSettings:
    """Class for Palworld settings. This class is used to manage the default settings string,
    default values, and descriptions for the Palworld game."""

    def __init__(self):
        self.default_settings_string = '[/Script/Pal.PalGameWorldSettings]\nOptionSettings=(Difficulty=None,DayTimeSpeedRate=1.000000,NightTimeSpeedRate=1.000000,ExpRate=1.000000,PalCaptureRate=1.000000,PalSpawnNumRate=1.000000,PalDamageRateAttack=1.000000,PalDamageRateDefense=1.000000,PlayerDamageRateAttack=1.000000,PlayerDamageRateDefense=1.000000,PlayerStomachDecreaceRate=1.000000,PlayerStaminaDecreaceRate=1.000000,PlayerAutoHPRegeneRate=1.000000,PlayerAutoHpRegeneRateInSleep=1.000000,PalStomachDecreaceRate=1.000000,PalStaminaDecreaceRate=1.000000,PalAutoHPRegeneRate=1.000000,PalAutoHpRegeneRateInSleep=1.000000,BuildObjectDamageRate=1.000000,BuildObjectDeteriorationDamageRate=1.000000,CollectionDropRate=1.000000,CollectionObjectHpRate=1.000000,CollectionObjectRespawnSpeedRate=1.000000,EnemyDropItemRate=1.000000,DeathPenalty=All,bEnablePlayerToPlayerDamage=False,bEnableFriendlyFire=False,bEnableInvaderEnemy=True,bActiveUNKO=False,bEnableAimAssistPad=True,bEnableAimAssistKeyboard=False,DropItemMaxNum=3000,DropItemMaxNum_UNKO=100,BaseCampMaxNum=128,BaseCampWorkerMaxNum=15,DropItemAliveMaxHours=1.000000,bAutoResetGuildNoOnlinePlayers=False,AutoResetGuildTimeNoOnlinePlayers=72.000000,GuildPlayerMaxNum=20,PalEggDefaultHatchingTime=72.000000,WorkSpeedRate=1.000000,bIsMultiplay=False,bIsPvP=False,bCanPickupOtherGuildDeathPenaltyDrop=False,bEnableNonLoginPenalty=True,bEnableFastTravel=True,bIsStartLocationSelectByMap=True,bExistPlayerAfterLogout=False,bEnableDefenseOtherGuildPlayer=False,CoopPlayerMaxNum=4,ServerPlayerMaxNum=32,ServerName="Default Palworld Server",ServerDescription="",AdminPassword="",ServerPassword="",PublicPort=8211,PublicIP="",RCONEnabled=False,RCONPort=25575,Region="",bUseAuth=True,BanListURL="https://api.palworldgame.com/api/banlist.txt")'  # pylint: disable=line-too-long
        self.default_values = {
            "Difficulty": "None",
            "DayTimeSpeedRate": "1.000000",
            "NightTimeSpeedRate": "1.000000",
            "ExpRate": "1.000000",
            "PalCaptureRate": "1.000000",
            "PalSpawnNumRate": "1.000000",
            "PalDamageRateAttack": "1.000000",
            "PalDamageRateDefense": "1.000000",
            "PlayerDamageRateAttack": "1.000000",
            "PlayerDamageRateDefense": "1.000000",
            "PlayerStomachDecreaceRate": "1.000000",
            "PlayerStaminaDecreaceRate": "1.000000",
            "PlayerAutoHPRegeneRate": "1.000000",
            "PlayerAutoHpRegeneRateInSleep": "1.000000",
            "PalStomachDecreaceRate": "1.000000",
            "PalStaminaDecreaceRate": "1.000000",
            "PalAutoHPRegeneRate": "1.000000",
            "PalAutoHpRegeneRateInSleep": "1.000000",
            "BuildObjectDamageRate": "1.000000",
            "BuildObjectDeteriorationDamageRate": "1.000000",
            "CollectionDropRate": "1.000000",
            "CollectionObjectHpRate": "1.000000",
            "CollectionObjectRespawnSpeedRate": "1.000000",
            "EnemyDropItemRate": "1.000000",
            "DeathPenalty": "All",
            "bEnablePlayerToPlayerDamage": "False",
            "bEnableFriendlyFire": "False",
            "bEnableInvaderEnemy": "True",
            "bActiveUNKO": "False",
            "bEnableAimAssistPad": "True",
            "bEnableAimAssistKeyboard": "False",
            "DropItemMaxNum": "3000",
            "DropItemMaxNum_UNKO": "100",
            "BaseCampMaxNum": "128",
            "BaseCampWorkerMaxNum": "15",
            "DropItemAliveMaxHours": "1.000000",
            "bAutoResetGuildNoOnlinePlayers": "False",
            "AutoResetGuildTimeNoOnlinePlayers": "72.000000",
            "GuildPlayerMaxNum": "20",
            "PalEggDefaultHatchingTime": "72.000000",
            "WorkSpeedRate": "1.000000",
            "bIsMultiplay": "False",
            "bIsPvP": "False",
            "bCanPickupOtherGuildDeathPenaltyDrop": "False",
            "bEnableNonLoginPenalty": "True",
            "bEnableFastTravel": "True",
            "bIsStartLocationSelectByMap": "True",
            "bExistPlayerAfterLogout": "False",
            "bEnableDefenseOtherGuildPlayer": "False",
            "CoopPlayerMaxNum": "4",
            "ServerPlayerMaxNum": "32",
            "ServerName": '"Default Palworld Server"',
            "ServerDescription": '""',
            "AdminPassword": '""',
            "ServerPassword": '""',
            "PublicPort": "8211",
            "PublicIP": '""',
            "RCONEnabled": "False",
            "RCONPort": "25575",
            "Region": '""',
            "bUseAuth": "True",
            "BanListURL": '"https://api.palworldgame.com/api/banlist.txt"',
            "bShowPlayerList": "False",
        }
        self.descriptions = {
            "Difficulty": "Adjusts the overall difficulty of the game.",
            "DayTimeSpeedRate": "Modifies the speed of in-game time during the day.",
            "NightTimeSpeedRate": "Modifies the speed of in-game time during the night.",
            "ExpRate": "Changes the experience gain rate for both players and creatures.",
            "PalCaptureRate": "Adjusts the rate at which Pal creatures can be captured.",
            "PalSpawnNumRate": "Adjusts the rate at which Pal creatures spawn.",
            "PalDamageRateAttack": "Fine-tunes Pal creature damage dealt.",
            "PalDamageRateDefense": "Fine-tunes Pal creature damage received.",
            "PlayerDamageRateAttack": "Fine-tunes player damage dealt.",
            "PlayerDamageRateDefense": "Fine-tunes player damage received.",
            "PlayerStomachDecreaseRate": "Adjusts the rate at which the player's stomach decreases.",
            "PlayerStaminaDecreaseRate": "Adjusts the rate at which the player's stamina decreases.",
            "PlayerAutoHPRegeneRate": "Adjusts the rate of automatic player health regeneration.",
            "PlayerAutoHpRegeneRateInSleep": "Adjusts the rate of automatic player health regeneration during sleep.",
            "PalStomachDecreaseRate": "Adjusts the rate at which Pal creature stomach decreases.",
            "PalStaminaDecreaseRate": "Adjusts the rate at which Pal creature stamina decreases.",
            "PalAutoHPRegeneRate": "Adjusts the rate of automatic Pal creature health regeneration.",
            "PalAutoHpRegeneRateInSleep": "Adjusts the rate of automatic Pal creature health regeneration during sleep.",
            "BuildObjectDamageRate": "Adjusts the rate at which built objects take damage.",
            "BuildObjectDeteriorationDamageRate": "Adjusts the rate at which built objects deteriorate.",
            "CollectionDropRate": "Adjusts the drop rate of collected items.",
            "CollectionObjectHpRate": "Adjusts the health of collected objects.",
            "CollectionObjectRespawnSpeedRate": "Adjusts the respawn speed of collected objects.",
            "EnemyDropItemRate": "Adjusts the drop rate of items from defeated enemies.",
            "DeathPenalty": "Defines the penalty upon player death (e.g., All, None).",
            "bEnablePlayerToPlayerDamage": "Enables or disables player-to-player damage.",
            "bEnableFriendlyFire": "Enables or disables friendly fire.",
            "bEnableInvaderEnemy": "Enables or disables invader enemies.",
            "bActiveUNKO": "Activates or deactivates UNKO (Unidentified Nocturnal Knock-off).",
            "bEnableAimAssistPad": "Enables or disables aim assist for controllers.",
            "bEnableAimAssistKeyboard": "Enables or disables aim assist for keyboards.",
            "DropItemMaxNum": "Sets the maximum number of dropped items in the game.",
            "DropItemMaxNum_UNKO": "Sets the maximum number of dropped UNKO items in the game.",
            "BaseCampMaxNum": "Sets the maximum number of base camps that can be built.",
            "BaseCampWorkerMaxNum": "Sets the maximum number of workers in a base camp.",
            "DropItemAliveMaxHours": "Sets the maximum time items remain alive after being dropped.",
            "bAutoResetGuildNoOnlinePlayers": "Automatically resets guilds with no online players.",
            "AutoResetGuildTimeNoOnlinePlayers": "Sets the time after which guilds with no online players are automatically reset.",
            "GuildPlayerMaxNum": "Sets the maximum number of players in a guild.",
            "PalEggDefaultHatchingTime": "Sets the default hatching time for Pal eggs.",
            "WorkSpeedRate": "Adjusts the overall work speed in the game.",
            "bIsMultiplay": "Enables or disables multiplayer mode.",
            "bIsPvP": "Enables or disables player versus player (PvP) mode.",
            "bCanPickupOtherGuildDeathPenaltyDrop": "Enables or disables the pickup of death penalty drops from other guilds.",
            "bEnableNonLoginPenalty": "Enables or disables non-login penalties.",
            "bEnableFastTravel": "Enables or disables fast travel.",
            "bIsStartLocationSelectByMap": "Enables or disables the selection of starting locations on the map.",
            "bExistPlayerAfterLogout": "Enables or disables the existence of players after logout.",
            "bEnableDefenseOtherGuildPlayer": "Enables or disables the defense of other guild players.",
            "CoopPlayerMaxNum": "Sets the maximum number of cooperative players in a session.",
            "ServerPlayerMaxNum": "Sets the maximum number of players allowed on the server.",
            "ServerName": "Sets the name of the Palworld server.",
            "ServerDescription": "Provides a description for the Palworld server.",
            "AdminPassword": "Sets the password for server administration.",
            "ServerPassword": "Sets the password for joining the Palworld server.",
            "PublicPort": "Sets the public port for the Palworld server.",
            "PublicIP": "Sets the public IP address for the Palworld server.",
            "RCONEnabled": "Enables or disables Remote Console (RCON) for server administration.",
            "RCONPort": "Sets the port for Remote Console (RCON) communication.",
            "Region": "Sets the region for the Palworld server.",
            "bUseAuth": "Enables or disables server authentication.",
            "BanListURL": "Sets the URL for the server's ban list.",
        }
        self.worldoptionsav_json_data_header = {
            "magic": 1396790855,
            "save_game_version": 3,
            "package_file_version_ue4": 522,
            "package_file_version_ue5": 1008,
            "engine_version_major": 5,
            "engine_version_minor": 1,
            "engine_version_patch": 1,
            "engine_version_changelist": 0,
            "engine_version_branch": "++UE5+Release-5.1",
            "custom_version_format": 3,
            "custom_versions": [
                ["40d2fba7-4b48-4ce5-b038-5a75884e499e", 7],
                ["fcf57afa-5076-4283-b9a9-e658ffa02d32", 76],
                ["0925477b-763d-4001-9d91-d6730b75b411", 1],
                ["4288211b-4548-16c6-1a76-67b2507a2a00", 1],
                ["1ab9cecc-0000-6913-0000-4875203d51fb", 100],
                ["4cef9221-470e-d43a-7e60-3d8c16995726", 1],
                ["e2717c7e-52f5-44d3-950c-5340b315035e", 7],
                ["11310aed-2e55-4d61-af67-9aa3c5a1082c", 17],
                ["a7820cfb-20a7-4359-8c54-2c149623cf50", 21],
                ["f6dfbb78-bb50-a0e4-4018-b84d60cbaf23", 2],
                ["24bb7af3-5646-4f83-1f2f-2dc249ad96ff", 5],
                ["76a52329-0923-45b5-98ae-d841cf2f6ad8", 5],
                ["5fbc6907-55c8-40ae-8e67-f1845efff13f", 1],
                ["82e77c4e-3323-43a5-b46b-13c597310df3", 0],
                ["0ffcf66c-1190-4899-b160-9cf84a46475e", 1],
                ["9c54d522-a826-4fbe-9421-074661b482d0", 44],
                ["b0d832e4-1f89-4f0d-accf-7eb736fd4aa2", 10],
                ["e1c64328-a22c-4d53-a36c-8e866417bd8c", 0],
                ["375ec13c-06e4-48fb-b500-84f0262a717e", 4],
                ["e4b068ed-f494-42e9-a231-da0b2e46bb41", 40],
                ["cffc743f-43b0-4480-9391-14df171d2073", 37],
                ["b02b49b5-bb20-44e9-a304-32b752e40360", 3],
                ["a4e4105c-59a1-49b5-a7c5-40c4547edfee", 0],
                ["39c831c9-5ae6-47dc-9a44-9c173e1c8e7c", 0],
                ["78f01b33-ebea-4f98-b9b4-84eaccb95aa2", 20],
                ["6631380f-2d4d-43e0-8009-cf276956a95a", 0],
                ["12f88b9f-8875-4afc-a67c-d90c383abd29", 45],
                ["7b5ae74c-d270-4c10-a958-57980b212a5a", 13],
                ["d7296918-1dd6-4bdd-9de2-64a83cc13884", 3],
                ["c2a15278-bfe7-4afe-6c17-90ff531df755", 1],
                ["6eaca3d4-40ec-4cc1-b786-8bed09428fc5", 3],
                ["29e575dd-e0a3-4627-9d10-d276232cdcea", 17],
                ["af43a65d-7fd3-4947-9873-3e8ed9c1bb05", 15],
                ["6b266cec-1ec7-4b8f-a30b-e4d90942fc07", 1],
                ["0df73d61-a23f-47ea-b727-89e90c41499a", 1],
                ["601d1886-ac64-4f84-aa16-d3de0deac7d6", 80],
                ["5b4c06b7-2463-4af8-805b-bf70cdf5d0dd", 10],
                ["e7086368-6b23-4c58-8439-1b7016265e91", 4],
                ["9dffbcd6-494f-0158-e221-12823c92a888", 10],
                ["f2aed0ac-9afe-416f-8664-aa7ffa26d6fc", 1],
                ["174f1f0b-b4c6-45a5-b13f-2ee8d0fb917d", 10],
                ["35f94a83-e258-406c-a318-09f59610247c", 41],
                ["b68fc16e-8b1b-42e2-b453-215c058844fe", 1],
                ["b2e18506-4273-cfc2-a54e-f4bb758bba07", 1],
                ["64f58936-fd1b-42ba-ba96-7289d5d0fa4e", 1],
                ["697dd581-e64f-41ab-aa4a-51ecbeb7b628", 88],
                ["d89b5e42-24bd-4d46-8412-aca8df641779", 41],
                ["59da5d52-1232-4948-b878-597870b8e98b", 8],
                ["26075a32-730f-4708-88e9-8c32f1599d05", 0],
                ["6f0ed827-a609-4895-9c91-998d90180ea4", 2],
                ["30d58be3-95ea-4282-a6e3-b159d8ebb06a", 1],
                ["717f9ee7-e9b0-493a-88b3-91321b388107", 16],
                ["430c4d19-7154-4970-8769-9b69df90b0e5", 15],
                ["aafe32bd-5395-4c14-b66a-5e251032d1dd", 1],
                ["23afe18e-4ce1-4e58-8d61-c252b953beb7", 11],
                ["a462b7ea-f499-4e3a-99c1-ec1f8224e1b2", 4],
                ["2eb5fdbd-01ac-4d10-8136-f38f3393a5da", 5],
                ["509d354f-f6e6-492f-a749-85b2073c631c", 0],
                ["b6e31b1c-d29f-11ec-857e-9f856f9970e2", 1],
                ["4a56eb40-10f5-11dc-92d3-347eb2c96ae7", 2],
                ["d78a4a00-e858-4697-baa8-19b5487d46b4", 18],
                ["5579f886-933a-4c1f-83ba-087b6361b92f", 2],
                ["612fbe52-da53-400b-910d-4f919fb1857c", 1],
                ["a4237a36-caea-41c9-8fa2-18f858681bf3", 5],
                ["804e3f75-7088-4b49-a4d6-8c063c7eb6dc", 5],
                ["1ed048f4-2f2e-4c68-89d0-53a4f18f102d", 1],
                ["fb680af2-59ef-4ba3-baa8-19b573c8443d", 2],
                ["9950b70e-b41a-4e17-bbcc-fa0d57817fd6", 1],
                ["ab965196-45d8-08fc-b7d7-228d78ad569e", 1],
            ],
            "save_game_class_name": "/Script/Pal.PalWorldOptionSaveGame",
        }
