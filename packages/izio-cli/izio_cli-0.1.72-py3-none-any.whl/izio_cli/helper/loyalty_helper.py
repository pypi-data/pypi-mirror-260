import os

from izio_cli.helper.console_helper import run_command


def setupFirebase(flavor, root):
    # get android firebase json
    run_command(
        [
            "cp",
            f"{root}{os.sep}firebase{os.sep}android{os.sep}google-services-{flavor}.json",
            f"{root}{os.sep}loyalty2_0{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}google-services.json",
        ],
        path=root,
        silent=True,
    )
    # get ios firebase json
    run_command(
        [
            "cp",
            f"{root}{os.sep}firebase{os.sep}apple{os.sep}GoogleService-Info-{flavor}.plist",
            f"{root}{os.sep}loyalty2_0{os.sep}ios{os.sep}Runner{os.sep}prod{os.sep}GoogleService-Info.plist",
        ],
        path=root,
        silent=True,
    )


def changeOnesignalIcons(root):
    base_path = f"{root}{os.sep}loyalty2_0{os.sep}android{os.sep}app{os.sep}src{os.sep}prod{os.sep}res"
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
        f"mipmap-hdpi{os.sep}ic_launcher.png": "drawable-mdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-mdpi{os.sep}ic_launcher.png": "drawable-hdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xhdpi{os.sep}ic_launcher.png": "drawable-xhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxhdpi{os.sep}ic_launcher.png": "drawable-xxhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxxhdpi{os.sep}ic_launcher.png": "drawable-xxxhdpi{os.sep}ic_stat_onesignal_default.png",
        f"mipmap-xxxhdpi{os.sep}ic_launcher.png": "drawable-xxxhdpi{os.sep}ic_onesignal_large_icon_default.png",
    }
    for file, new_file in files.items():
        run_command(
            ["cp", f"{base_path}{os.sep}{file}", f"{base_path}{os.sep}{new_file}"],
            path=root,
            silent=True,
        )


def changeAppIcon(root, appIconPath):
    with open(
        f"{root}{os.sep}loyalty2_0{os.sep}flutter_launcher_icons-prod.yaml", "r"
    ) as file:
        data = file.read()
        actualIcon = data.split("image_path: ")[1].split("\n")[0]
        data = data.replace(f"image_path: {actualIcon}", f"image_path: {appIconPath}")
        with open(
            f"{root}{os.sep}loyalty2_0{os.sep}flutter_launcher_icons-prod.yaml", "w"
        ) as file:
            file.write(data)

    with open(
        f"{root}{os.sep}loyalty2_0{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj",
        "r",
    ) as file:
        data = file.read()
        run_command(
            [
                "dart",
                "run",
                "flutter_launcher_icons:main",
            ],
            path=f"{root}{os.sep}loyalty2_0",
            silent=True,
        )
        with open(
            f"{root}{os.sep}loyalty2_0{os.sep}ios{os.sep}Runner.xcodeproj{os.sep}project.pbxproj",
            "w",
        ) as file:
            file.write(data)


def setupEnvFile(flavor, root):
    run_command(
        [
            "cp",
            f"{root}{os.sep}loyalty2_0{os.sep}envs{os.sep}{flavor}.env",
            f"{root}{os.sep}loyalty2_0{os.sep}.env",
        ],
        path=root,
        silent=True,
    )
    run_command(
        [
            "dart",
            "run",
            "app_env",
        ],
        path=f"{root}{os.sep}loyalty2_0",
        silent=True,
    )


def getEnv(flavor, root):
    with open(f"{root}{os.sep}loyalty2_0{os.sep}envs{os.sep}{flavor}.env", "r") as file:
        data = file.read()
        bundleId = data.split("LOYALTY_APP_ID=")[1].split("\n")[0]
        print(f"Bundle ID: {bundleId}")
        appName = data.split("LOYALTY_APP_NAME_BUILD=")[1].split("\n")[0]
        print(f"App Name: {appName}")
        flavor = data.split("LOYALTY_APP_FLAVOR=")[1].split("\n")[0]
        print(f"Flavor: {flavor}")
        appIconPath = data.split("LOYALTY_PROJECT_ICON_PATH=")[1].split("\n")[0]
        print(f"App Icon Path: {appIconPath}")
    return flavor, bundleId, appName, appIconPath
