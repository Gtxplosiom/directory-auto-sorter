const { app, Menu, Tray, dialog } = require('electron');
const { exec } = require('child_process');
const os = require('os')

let tray = null;

// default user directories
let userHome = os.homedir();
let userDesktop = userHome + '\\Desktop';   // default dir for sort

// sorting modes
let acceptedArgs = ['createDir', 'dateSort'];

// store/remember radio button state after context menu update
let createDir = true;
let dateSort = false;

// command structure. below are the initial state
let baseCommand = 'python services/sort.py';
let currentDir = `\"${userDesktop}\"`;
let currentMode = acceptedArgs[0];

app.whenReady().then(() => {
  tray = new Tray('assets/sort.ico');

  // one click sort
  tray.addListener('click', () => {

    let command = baseCommand + ' ' + currentMode + ' ' + currentDir;

    console.log(command);

    execCommand(command);
  });

  // executes python scripts
  const execCommand = (command) => {
    try {
        exec(command, (error, stdout, stderr) => {
            console.log(stdout);
        });
    } catch (err) {
        console.log(err);
    }
  }

  // updates current target directory
  const updateDir = (dir) => {
    currentDir = dir;
  }

  // updates current sorting mode
  const updateMode = (mode) => {
    currentMode = mode;
  }

  const updateTooltip = () => {
    tray.setToolTip(`Tap the Icon to sort ${currentDir} or Right-click for options`);
  }

  // add new path to target as well as 'remember' paths previously targeted
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
