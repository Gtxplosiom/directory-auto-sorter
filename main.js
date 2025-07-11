const { app, Menu, Tray } = require('electron');
const { exec } = require('child_process');

let tray = null;

let acceptedArgs = [' createDir', ' categorySort']
let baseCommand = 'python services/sort.py'

app.whenReady().then(() => {
  tray = new Tray('assets/sort.png')

  tray.addListener('click', () => {
    console.log('Sorting...');

    exec(baseCommand, (error, stdout, stderr) => {
        console.log(stdout);
    });
  });

  const contextMenu = Menu.buildFromTemplate([
    {label: 'Create Directory', type: 'checkbox', checked: false, click: (createDir) => {
        console.log('toggling create directory');
        createDir.checked ? baseCommand += acceptedArgs[0] : baseCommand = baseCommand.replace(acceptedArgs[0], '');
    }},
    {label: 'Categorized Sorting', type: 'checkbox', checked: false, click: (categorySort) => {
        console.log('toggling cateogory sort')
        categorySort.checked ? baseCommand += acceptedArgs[1] : baseCommand = baseCommand.replace(acceptedArgs[1], '');
    }},
    {label: 'Exit', click: () => {
        console.log('Exiting...');
        app.exit();
    }}
  ]);

  tray.setToolTip('Desktop Auto Sorter');
  tray.setContextMenu(contextMenu);
})
