const { app, Menu, Tray, dialog } = require('electron');
const { exec } = require('child_process');
const os = require('os')

let tray = null;

let userHome = os.homedir();
let userDesktop = userHome + '\\Desktop';   // default dir for sort
let currentDir = userDesktop;

let acceptedArgs = [' createDir', ' categorySort'];

let baseCommand = `python services/sort.py ${currentDir}`;
let activatedCommand = baseCommand;

app.whenReady().then(() => {
  tray = new Tray('assets/sort.png')

  activatedCommand += acceptedArgs[0];

  tray.addListener('click', () => {
    exec(activatedCommand, (error, stdout, stderr) => {
        console.log(stdout);
    });
  });

  let targetDirItems = [
    {label: '+', click: () => {
        dialog.showOpenDialog({
            title: 'Select a folder you want to target',
            properties: ['openDirectory']
        }).then((result) => {
            if (!result.canceled) {
                targetDirItems.push({label: `${result.filePaths[0]}`});
            }
            updateContextMenu();
        }).catch((error) => {
            console.log(error);
        })
    }}
  ];

  function updateContextMenu() {
    let contextMenuItems = [
        {label: 'Target Directory', submenu: targetDirItems},
        {label: 'Create Directory', type: 'radio', checked: true, click: () => {
            activatedCommand = baseCommand;
            activatedCommand = activatedCommand += acceptedArgs[0];
        }},
        {label: 'Categorized Sorting', type: 'radio', checked: false, click: () => {
            activatedCommand = baseCommand;
            activatedCommand = activatedCommand += acceptedArgs[1];
        }},
        {label: 'Exit', click: () => {
            console.log('Exiting...');
            app.exit();
        }}
    ];
    
    const newContextMenu = Menu.buildFromTemplate(contextMenuItems);
    tray.setContextMenu(newContextMenu);
  }

  tray.setToolTip('Desktop Auto Sorter');
  updateContextMenu();
})
