# python-azure-app

See [article](https://medium.com/enefitit/tutorial-of-python-in-azure-app-service-ed348887dfc0) on Tutorial of Python in Azure App Service.

## Quick Note

When the App Service is being deployed, specially when it is new, the log shows that it goes through several cycles of starting and stopping its container. It seems to do this until some goal is reached. My best guess is that by the time `startup.sh` is executed then it keeps that container. If you ssh using Kudu, you can see the files that startup.sh copies to /home/site/wwwroot. When the App Service is not new and the log says the container is stopped. It will actually never start again it seems.

Please note that you can create a second App Service under the same App Service plan if you use the same Zone, e.g. Central US, and the same tier B1.

## Process

### Build

#### VueJS

Run:
```
cd ~/dev/python-azure-app/client
npm i
npm run build
```

#### Python

Modify server/app.py:
```
app = Flask(__name__, static_folder='/Users/owpalmer/dev/python-azure-app/dist', static_url_path='/')
```

Creating Python Virtual Environment:
```
cd ~/dev/python-azure-app
python3 -m venv .venv  
source .venv/bin/activate  
pip3 install -r requirements.txt 
```

### Test

Browse to:
http://localhost:8000/
http://localhost:8000/prices
http://localhost:8000/files



## Installation

### VS Code

In VS Code, go to Azure extension icon.

Create App Service (B1 in CentralUS); let name = python-vue-app-0006.

See sample [log](./README.md_files/app-create-log.png).  

### Preparing Environment

Go to Portal.

Go to Home.

Go to Resource groups.

Click `appsvc_linux_centralus_basic.

Click python-azure-app-0006 w/ as type App Service.

Click menu Settings > Environment variables and click Add.

Specify PYTHONUNBUFFERED=1.

Click menu Configuration > Stack settings > Startup command.

Specify `startup.sh`.

### Deploying App v1

Go to VS Code.

Go to Project Explorer where your source files are displayed.

Right-click in the empty space below the last file.

Select Deploy to Web App.

See [VS Code log](./README.md_files/app-deploy-log.jpg).

See sample deployment [log](./README.md_files/sample-deploy-log.txt).

### Deploying App v2

Go to VS Code.

Go to Project Explorer where your source files are displayed.

Press Cmd+Shift+P on macOS.

Run `Tasks: Run Task`.

Choose `Package Azure deploy`.

Right-click in the empty space below the last file.

Select Deploy to Web App.

See [VS Code log](./README.md_files/app-deploy-log.jpg).

See sample deployment [log](./README.md_files/sample-deploy-log.txt).

### Test

Wait for log to show equivalent of the following lines:
```
2026-09-28T02:47:40.1216960Z Site started.
2026-09-28T02:47:40.1231497Z State: Started, Action: None, LastError: ContainerStartupFailure, LastErrorTimestamp: 09/28/2026 02:45:25, LastErrorDetails: Container exited with exit code 3 during startup after 90.1s. Please inspect your container logs for more details., Details: Site started at 09/28/2026 02:47:40 (UTC), DetailsLevel: INFO
2026-09-28T02:47:40.2350734Z Site is running with patch version PYTHON-3.11.15
```

Go to Portal.

Go to Home.

Go to Resource groups.

Click `appsvc_linux_centralus_basic.

Click python-azure-app-0006 w/ as type App Service.

Click the Browse button at the top of the page.

## Helpful Operations

### Troubleshooting w/ Development Tools

Click menu Development Tools > Advanced Tools.

Click the Go link.

Click Log Stream to observe log.

Or click SSH -Kudu to login.

### Controlling via AZ Cli

Tail log:
```
az login
az webapp log tail --name python-vue-app-0000 --resource-group appsvc_linux_centralus_basic
az webapp restart --name python-vue-app-0000 --resource-group appsvc_linux_centralus_basic
```

## See Also

### Show Files

app.py:
```
def build_directory_report():
    directories = [os.getcwd(), "/home/site/wwwroot", "/home/site/wwwroot/dist"]
    lines = ["Running the Flask application..."]

    for directory in directories:
        lines.append(f"Directory: {directory}")
        if not os.path.isdir(directory):
            lines.extend(["All items: unavailable", "Files only: unavailable", ""])
            continue

        entries = os.listdir(directory)
        files_only = [f for f in entries if os.path.isfile(os.path.join(directory, f))]
        lines.extend([f"All items: {entries}", f"Files only: {files_only}", ""])
    report = "\n".join(lines)
    print(report)
    return report

@app.route('/files')
def logs():
    report = build_directory_report()
    return Response(report, mimetype='text/plain')
```

https://python-azure-app-0006-ckhdfne6dddafkaf.centralus-01.azurewebsites.net/logs
```
Starting the Flask application...
Current Directory: /tmp/8df1d11d94dad47

All items: ['README.md', 'requirements.txt', 'antenv', 'calculator.py', '__pycache__', 'README-badlog.txt', '.gitignore', 'app.py', 'startup.sh', '.venv']
Files only: ['README.md', 'requirements.txt', 'calculator.py', 'README-badlog.txt', '.gitignore', 'app.py', 'startup.sh']
```

### Configuring Environment

```
PYTHONUNBUFFERED=1
```

### Environment variables

```
WEBSITE_SSH_PASSWORD=Docker!
SHELL=/bin/bash
APPSETTING_ScmType=None
WEBSITE_SITE_NAME=python-azure-app-0006
NUGET_XMLDOC_MODE=skip
WEBSITE_DEFAULT_HOSTNAME=python-azure-app-0006-ckhdfne6dddafkaf.centralus-01.azurewebsites.net
WEBSITE_AUTH_ENCRYPTION_KEY=35BDFDFAFC7ACB05465AB23B8BF7BAEFD91C0360E6D2EEC69EF3827BF38E619E
PYTHONUNBUFFERED=1
WEBSITE_SSH_USER=root
WEBSITE_SKU=Basic
HOSTNAME=0d0d470b360f
ORYX_ENABLE_EXTERNAL_ACR_SDK_PROVIDER=true
LANGUAGE=C.UTF-8
ApplicationInsightsAgent_EXTENSION_VERSION=~3
APPSETTING_APPLICATIONINSIGHTSAGENT_EXTENSION_ENABLED=true
WEBSITE_INSTANCE_ID=6988dec20f7c9bb73c739ef04db98faf5f49e2286cba471b5935203f8f415c4a
APPSETTING_SCM_USE_LIBGIT2SHARP_REPOSITORY=0
DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
APPSETTING_WEBSITE_DEFAULT_HOSTNAME=python-azure-app-0006-ckhdfne6dddafkaf.centralus-01.azurewebsites.net
WEBSITE_AUTH_SIGNING_KEY=71CF682F9585628703FC37167B74370F7106653F15447BBEA7D10FAE133728D9
PWD=/tmp
LOGNAME=kudu_ssh_user
PORT=8181
REGION_NAME=centralus
WEBSITE_PYTHON_VERSION=3.11
APPSETTING_WEBSITE_SITE_NAME=python-azure-app-0006
NUM_CORES=1
ORYX_AI_CONNECTION_STRING=InstrumentationKey=4aadba6b-30c8-42db-9b93-024d5c62b887
WEBSITE_OWNER_NAME=bec56cb3-2b74-4a4f-999c-e1d2e9ad9364+appsvc_linux_centralus_basic-CentralUSwebspace-Linux
MOTD_SHOWN=pam
ORIGINAL_PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOME=/home
LANG=C.UTF-8
KUDU_INSTALL_LEGACY_WEBSSH2=true
KUDU_WEBSSH_PORT=3000
DEBIAN_FLAVOR=bookworm
SCM_DO_BUILD_DURING_DEPLOYMENT=true
APPLICATIONINSIGHTSAGENT_EXTENSION_ENABLED=true
ORYX_ENV_TYPE=AppService
APPDATA=/opt/Kudu/local
WEBSITE_USE_DIAGNOSTIC_SERVER=true
OS_FLAVOR=bookworm
APPSETTING_ApplicationInsightsAgent_EXTENSION_VERSION=~3
SSH_CONNECTION=127.0.0.1 33184 127.0.0.6 22
DYNAMIC_INSTALL_ENABLED=true
WEBSITE_RESOURCE_GROUP=appsvc_linux_centralus_basic
WEBSITE_STACK=PYTHON
COMPUTERNAME=lw1sdlwk0000F3
WEBSITE_ISOLATION=lxc
APPSETTING_PYTHONUNBUFFERED=1
APPSETTING_WEBSITE_HTTPLOGGING_RETENTION_DAYS=7
KUDU_APPPATH=/opt/Kudu
WEBSITE_ROLE_INSTANCE_ID=543
WEBSITE_HOME_STAMPNAME=waws-prod-dm1-377
TERM=xterm-color
USER=kudu_ssh_user
MSBUILDCOPYWITHOUTDELETE=1
FRAMEWORK=PYTHON
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=32d35fec-3fcc-4c52-bd39-72a4a441501e;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/;ApplicationId=8028a4f7-5983-4e55-b8d3-06e8a1101f0e
ScmType=None
WEBSITE_HTTPLOGGING_RETENTION_DAYS=7
PLATFORM_VERSION=110.0.7.49
SHLVL=1
ORYX_SDK_STORAGE_BASE_URL=https://oryx-cdn.microsoft.io
WEBSITE_SSH_ENABLED=1
LINUX_FX_VERSION=PYTHON|3.11
ORYX_ENABLE_EXTERNAL_SDK_PROVIDER=true
DOTNET_RUNNING_IN_CONTAINER=true
DOTNET_USE_POLLING_FILE_WATCHER=true
ENABLE_DYNAMIC_INSTALL=true
WEBSITE_WEBSERVER_LOGGING_ENABLED=0
WEBSITE_LINUX_ASSETS_BUILD_ID=180648184
NUGET_PACKAGES=/var/nuget
APPSETTING_WEBSITE_AUTH_ENABLED=False
SSH_USER_PASSWORD=i1g3jx86e7kd
APPSETTING_APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=32d35fec-3fcc-4c52-bd39-72a4a441501e;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/;ApplicationId=8028a4f7-5983-4e55-b8d3-06e8a1101f0e
SSH_CLIENT=127.0.0.1 33184 22
ORYX_PATHS=/opt/oryx:/opt/yarn/stable/bin:/opt/hugo/lts
ENABLE_ORYX_BUILD=true
SSH_USER_NAME=kudu_ssh_user
WEBSITE_HOSTNAME=python-azure-app-0006-ckhdfne6dddafkaf.centralus-01.azurewebsites.net
WEBSITE_DEPLOYMENT_ID=python-azure-app-0006
KUDU_ENV=Bookworm
LC_ALL=C.UTF-8
APPSETTING_SCM_DO_BUILD_DURING_DEPLOYMENT=true
PATH=/opt/oryx:/opt/yarn/stable/bin:/opt/hugo/lts:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
WEBSITE_AUTH_ENABLED=False
FRAMEWORK_VERSION=3.11
KUDU_RUN_USER=u3d7b8dd6d29ff55fbdda9c
KUDU_BUILD_VERSION=20260818.3
SSH_TTY=/dev/pts/0
NODE_VERSION=
WEBSITE_PLATFORM_RELEASE_CHANNEL=standard
DEBIAN_FRONTEND=noninteractive
ORYX_ENV_NAME=~1python-azure-app-0006
OLDPWD=/home
_=/usr/bin/env
```

### Deployment Log

```
12:43:47 AM python-azure-app-0006: Zip package size: 7.73 MB
12:43:49 AM python-azure-app-0006: Fetching changes.
12:43:50 AM python-azure-app-0006: Starting  LocalZipHandler
12:43:50 AM python-azure-app-0006: Cleaning up temp folders from previous zip deployments and extracting pushed zip file /tmp/zipdeploy/0b28b052-e73e-46c4-877c-7e259cd51916.zip (7.37 MB) to /tmp/zipdeploy/extracted
12:43:56 AM python-azure-app-0006: Updating submodules.
12:43:57 AM python-azure-app-0006: Preparing deployment for commit id '6f487d84-7'.
12:43:58 AM python-azure-app-0006: PreDeployment: context.CleanOutputPath False
12:43:59 AM python-azure-app-0006: PreDeployment: context.OutputPath /home/site/wwwroot
12:43:59 AM python-azure-app-0006: Repository path is /tmp/zipdeploy/extracted
12:43:59 AM python-azure-app-0006: Running oryx build...
12:43:59 AM python-azure-app-0006: Command: oryx build /tmp/zipdeploy/extracted -o /home/site/wwwroot --platform python --platform-version 3.11 -p virtualenv_name=antenv --log-file /tmp/build-debug.log  -i /tmp/8df1d1b1c0257f2 --compress-destination-dir | tee /tmp/oryx-build.log
12:44:09 AM: Deployment to "python-azure-app-0006" completed.
```

### Oryx Log

```
kudu_ssh_user@0d0d470b360f:/tmp$ cat oryx-build.log 
Operation performed by Microsoft Oryx, https://github.com/Microsoft/Oryx
You can report issues at https://github.com/Microsoft/Oryx/issues

Oryx Version: 0.2.20260728.2+203b718c5847f8ff2fa0f9aaeb1987e6b1bd30d7, Commit: 203b718c5847f8ff2fa0f9aaeb1987e6b1bd30d7, ReleaseTagName: 20260728.2

Build Operation ID: 4a5eae8cf6e9774a
Repository Commit : 6f487d84-7b76-466a-bcf9-d9ca19736a84
OS Type           : bookworm
Image Type        : githubactions

Primary SDK Storage URL: https://oryx-cdn.microsoft.io
Backup SDK Storage URL: 
ACR SDK Registry URL: (not set)
SDK provider status:
  External ACR SDK provider: Enabled
  External SDK provider: Enabled
  Direct ACR SDK provider: Disabled
  Blob SDK provider: Enabled
External ACR SDK provider is enabled. Only using user-specified platform: python
Detecting platforms...
External ACR provider resolved version '3.11.15' for python.
Version resolved using external ACR SDK provider.
Detected following platforms:
  python: 3.11.15
Requesting SDK from ACR via external provider: python 3.11.15 (bookworm)
Successfully pulled SDK from ACR via external provider: python 3.11.15
SDK for 'python' version '3.11.15' fetched via external ACR provider.
Version '3.11.15' of platform 'python' is not installed. Generating script to install it...

Using intermediate directory '/tmp/8df1d1b1c0257f2'.

Copying files to the intermediate directory...
Copying files to intermediate directory done in 3 sec(s).

Source directory     : /tmp/8df1d1b1c0257f2
Destination directory: /home/site/wwwroot

Installing platform...

Downloading and extracting 'python' version '3.11.15' to '/tmp/oryx/platforms/python/3.11.15'...
Detected image debian flavor: bookworm.
SDK binary download was skipped. Looking for cached tarball...
Found tarball at /var/OryxAcrSdks/python/python-bookworm-3.11.15.tar.gz
```

### VS Code Files

### settings.json

```
{
    "appService.defaultWebAppToDeploy": "/subscriptions/bec56cb3-2b74-4a4f-999c-e1d2e9ad9364/resourceGroups/appsvc_linux_centralus_basic/providers/Microsoft.Web/sites/python-azure-app-2322",
    "appService.deploySubpath": ".deploy-package"
}
```

tasks.json:
```
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Package Azure deploy",
      "type": "shell",
      "command": "./scripts/package_for_azure.sh",
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": []
    }
  ]
}
```
