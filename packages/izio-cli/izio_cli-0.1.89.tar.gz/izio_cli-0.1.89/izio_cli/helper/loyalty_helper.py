import os
import shutil
from izio_cli.helper.console_helper import run_command
from rich.table import Table


def setupFirebase(flavor, root, project="loyalty2_0"):
    print(f"Setting up firebase Android for {flavor} flavor, in {project} project... from {root}...")
    # get android firebase json
    shutil.copy2(f"{root}{os.sep}firebase{os.sep}android{os.sep}google-services-{flavor}.json",
            f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}google-services.json",)
    # run_command(
    #     [
    #         "cp",
    #         f"{root}{os.sep}firebase{os.sep}android{os.sep}google-services-{flavor}.json",
    #         f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}google-services.json",
    #     ],
    #     path=root,
    #     silent=False,
    # )
    print(f"Setting up firebase iOS for {flavor} flavor, in {project} project... from {root}...")
    # get ios firebase json
    shutil.copy2(f"{root}{os.sep}firebase{os.sep}apple{os.sep}GoogleService-Info-{flavor}.plist",
            f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner{os.sep}prod{os.sep}GoogleService-Info.plist",)
    # run_command(
    #     [
    #         "cp",
    #         f"{root}{os.sep}firebase{os.sep}apple{os.sep}GoogleService-Info-{flavor}.plist",
    #         f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner{os.sep}prod{os.sep}GoogleService-Info.plist",
    #     ],
    #     path=root,
    #     silent=False,
    # )


def changeOnesignalIcons(root, project="loyalty2_0", cd: bool = False):
    if not cd:
        print(f"Skippping Onesignal icons setup on a non cd environment")
        return
    
    base_path = f"{root}{os.sep}{project}{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}res"
    # create drwable folders
    folders = [
        "drawable-mdpi",
        "drawable-hdpi",
        "drawable-xhdpi",
        "drawable-xxhdpi",
        "drawable-xxxhdpi",
    ]
    for folder in folders:
        os.makedirs(f"{base_path}{os.sep}{folder}", exist_ok=True)

    files = {
        f"mipmap-hdpi{os.sep}ic_launcher.png": f"drawable-mdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-mdpi{os.sep}ic_launcher.png": f"drawable-hdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xhdpi{os.sep}ic_launcher.png": f"drawable-xhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxhdpi{os.sep}ic_launcher.png": f"drawable-xxhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxxhdpi{os.sep}ic_launcher.png": f"drawable-xxxhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxxhdpi{os.sep}ic_launcher.png": f"drawable-xxxhdpi{os.sep}ic_onesignal_large_icon_default.png",
    }
    for file, new_file in files.items():
        shutil.copy2(f"{base_path}{os.sep}{file}", f"{base_path}{os.sep}{new_file}")
        # run_command(
        #     ["cp", f"{base_path}{os.sep}{file}", f"{base_path}{os.sep}{new_file}"],
        #     path=root,
        #     silent=True,
        # )


def changeAppIcon(root, appIconPath, project="loyalty2_0"):
    with open(
        f"{root}{os.sep}{project}{os.sep}flutter_launcher_icons-prod.yaml", "r"
    ) as file:
        data = file.read()
        actualIcon = data.split("image_path: ")[1].split("\n")[0]
        data = data.replace(f"image_path: {actualIcon}", f"image_path: {appIconPath}")
        with open(
            f"{root}{os.sep}{project}{os.sep}flutter_launcher_icons-prod.yaml", "w"
        ) as file:
            file.write(data)

    shutil.copy2(
        f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj",
        f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj.bak",
    )

    run_command(
            "dart run flutter_launcher_icons:main",
            path=f"{root}{os.sep}{project}",
            silent=True,
    )
    # apaga o arquivo antigo
    os.remove(f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj")
    # volta o backup
    shutil.copy2(
        f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj.bak",
        f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj",
    )
    # apaga o backup
    os.remove(f"{root}{os.sep}{project}{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj.bak")



def setupEnvFile(flavor, root, project="loyalty2_0"):
    shutil.copy2(f"{root}{os.sep}{project}{os.sep}envs{os.sep}{flavor}.env",
            f"{root}{os.sep}{project}{os.sep}.env",)
    # run_command(
    #     [
    #         "cp",
    #         f"{root}{os.sep}{project}{os.sep}envs{os.sep}{flavor}.env",
    #         f"{root}{os.sep}{project}{os.sep}.env",
    #     ],
    #     path=root,
    #     silent=True,
    # )
    run_command(
        "dart run app_env",
        path=f"{root}{os.sep}{project}",
        silent=True,
    )


def getEnv(flavor, root, console, project="loyalty2_0"):
    with open(f"{root}{os.sep}{project}{os.sep}envs{os.sep}{flavor}.env", "r") as file:
        data = file.read()
        bundleId = data.split("LOYALTY_APP_ID=")[1].split("\n")[0]
        appName = data.split("LOYALTY_APP_NAME_BUILD=")[1].split("\n")[0]
        flavor = data.split("LOYALTY_APP_FLAVOR=")[1].split("\n")[0]
        appIconPath = data.split("LOYALTY_PROJECT_ICON_PATH=")[1].split("\n")[0]

        table = Table(title="Env File")
        table.add_column("Key", style="green bold", )
        table.add_column("Value")
        table.add_row("Bundle ID", bundleId)
        table.add_row("App Name", appName)
        table.add_row("Flavor", flavor)
        table.add_row("App Icon Path", appIconPath)
        console.print(table)
    return flavor, bundleId, appName, appIconPath
