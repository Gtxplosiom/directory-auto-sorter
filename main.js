const { app, Menu, Tray, dialog } = require('electron');
const { exec } = require('child_process');
const os = require('os')
const path = require('path');
const isDev = !app.isPackaged;

// debugging mode or actual app na para di magkaloko an mga assets ngan an connection nira ha user directories 
const iconPath = isDev
  ? path.join(__dirname, 'assets', 'sort.ico')
  : path.join(process.resourcesPath, 'assets', 'sort.ico');

const scriptPath = isDev
  ? path.join(__dirname, 'services', 'sort.py')
  : path.join(process.resourcesPath, 'services', 'sort.py');

let tray = null;

// default user directories
let userHome = os.homedir();
let userDesktop = userHome + '\\Desktop';   // default dir for sort

// an current nga sorting modes
let acceptedArgs = ['createDir', 'dateSort'];

// store/remember radio button state after context menu update
let createDir = true;
let dateSort = false;

// command structure. below are the initial state
let baseCommand = `python \"${scriptPath}\"`;
let currentDir = `\"${userDesktop}\"`;
let currentMode = acceptedArgs[0];

app.whenReady().then(() => {
  tray = new Tray(iconPath);

  // one click sort
  tray.addListener('click', () => {

    let command = baseCommand + ' ' + currentMode + ' ' + currentDir;

    console.log(command);

    execCommand(command);
  });

  // nag e-execute han python script
  const execCommand = (command) => {
    try {
        exec(command, (error, stdout, stderr) => {
            console.log(stdout);
        });
    } catch (err) {
        console.log(err);
    }
  }

  // helper method para ma update an state han current directory
  const updateDir = (dir) => {
    currentDir = dir;
  }

  // usame as this para ma update kada traversal ha ui
  const updateMode = (mode) => {
    currentMode = mode;
  }

  const updateTooltip = () => {
    tray.setToolTip(`Tap the Icon to sort ${currentDir} or Right-click for options`);
  }

  // TODO: ig implement so an mga na add hin users na recent 10 na directories ma reremember kada open han app
  // kay yana na fo-forget kada shutdown (kun gin startup mo) or exit and open again (or restart)
  // TODO: ig pa auto startup app 
  let targetDirItems = [
    {label: '(Default) Desktop', type: 'radio', checked: true, click: () => {
        updateDir(userDesktop);
        updateTooltip();
    }},
    {label: '+', click: () => {
        dialog.showOpenDialog({
            title: 'Select a folder you want to target',
            properties: ['openDirectory']
        }).then((result) => {
            if (!result.canceled) {
                targetDirItems.push({label: `${result.filePaths[0]}`, type: 'radio', checked: false, click: (pathItem) => {
                    updateDir(pathItem.label);
                    updateTooltip();
                }});
            }
            updateContextMenu();
        }).catch((error) => {
            console.log(error);
        })
    }}
  ];

  const updateContextMenu = () => {
    let contextMenuItems = [
        {label: 'Target Directory', submenu: targetDirItems},
        {label: '(Default) File-type Sorting', type: 'radio', checked: createDir, click: () => {
            dateSort = false;    // TODO: enclose these in an object
            createDir = true;
            updateMode(acceptedArgs[0]);
            updateTooltip();
        }},
        {label: 'Date Sorting', type: 'radio', checked: dateSort, click: () => {
            createDir = false;
            dateSort = true;
            updateMode(acceptedArgs[1]);
            updateTooltip();
        }},
        {label: 'Exit', click: () => {
            console.log('Exiting...');
            app.exit();
        }}
    ];

    const newContextMenu = Menu.buildFromTemplate(contextMenuItems);

    updateTooltip();

    tray.setContextMenu(newContextMenu);
  }

  updateContextMenu();
})
