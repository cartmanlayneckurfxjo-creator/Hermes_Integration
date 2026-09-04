const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const http = require('http');

let currentProfile = 'antigravity';
let statusBarItem;

function getHermesDir() {
    if (process.env.HERMES_DIR && fs.existsSync(process.env.HERMES_DIR)) {
        return process.env.HERMES_DIR;
    }
    if (fs.existsSync('F:\\AI\\hermes')) {
        return 'F:\\AI\\hermes';
    }
    const homeHermes = path.join(process.env.USERPROFILE || process.env.HOME || '', '.hermes');
    if (fs.existsSync(homeHermes)) {
        return homeHermes;
    }
    return 'F:\\AI\\hermes';
}

function getAvailableProfiles() {
    const hermesDir = getHermesDir();
    const profilesDir = path.join(hermesDir, 'profiles');
    if (fs.existsSync(profilesDir)) {
        try {
            return fs.readdirSync(profilesDir, { withFileTypes: true })
                .filter(d => d.isDirectory())
                .map(d => d.name);
        } catch (e) {
            return ['antigravity'];
        }
    }
    return ['antigravity'];
}

function checkProxyOnline(port = 20128) {
    return new Promise((resolve) => {
        const req = http.get({ host: '127.0.0.1', port, path: '/v1/models', timeout: 800 }, (res) => {
            resolve(res.statusCode < 500);
        });
        req.on('error', () => resolve(false));
        req.on('timeout', () => { req.destroy(); resolve(false); });
    });
}

function updateStatusBar(proxyOnline = null) {
    if (!statusBarItem) return;
    const proxyStatus = proxyOnline === true ? '⚡' : (proxyOnline === false ? '⚪' : '');
    statusBarItem.text = `$(hubot) Hermes [${currentProfile}] ${proxyStatus}`.trim();
    statusBarItem.tooltip = `Hermes Agent Status\nBot Profile: ${currentProfile}\nClick to open quick actions`;
    statusBarItem.show();
}

function activate(context) {
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 95);
    statusBarItem.command = 'hermes.openMenu';
    context.subscriptions.push(statusBarItem);

    checkProxyOnline().then(online => updateStatusBar(online));
    const interval = setInterval(() => {
        checkProxyOnline().then(online => updateStatusBar(online));
    }, 15000);
    context.subscriptions.push({ dispose: () => clearInterval(interval) });

    const menuCmd = vscode.commands.registerCommand('hermes.openMenu', async () => {
        const proxyOnline = await checkProxyOnline();
        const items = [
            {
                label: '$(play) Run ACP Task',
                description: 'Send task to Hermes via ACP runner'
            },
            {
                label: `$(person) Active Bot: ${currentProfile}`,
                description: 'Switch bot profile'
            },
            {
                label: `$(radio-tower) Local Gateway: ${proxyOnline ? 'Online (:20128)' : 'Offline'}`,
                description: 'Check local AI proxy status'
            },
            {
                label: '$(folder) Open Hermes Directory',
                description: getHermesDir()
            }
        ];

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: 'Hermes Agent Actions'
        });

        if (!selected) return;

        if (selected.label.includes('Run ACP Task')) {
            vscode.commands.executeCommand('hermes.runTask');
        } else if (selected.label.includes('Active Bot')) {
            vscode.commands.executeCommand('hermes.switchProfile');
        } else if (selected.label.includes('Open Hermes Directory')) {
            const hDir = getHermesDir();
            vscode.env.openExternal(vscode.Uri.file(hDir));
        } else if (selected.label.includes('Local Gateway')) {
            vscode.window.showInformationMessage(`Gateway (port 20128) is ${proxyOnline ? 'ONLINE' : 'OFFLINE'}`);
        }
    });
    context.subscriptions.push(menuCmd);

    const profileCmd = vscode.commands.registerCommand('hermes.switchProfile', async () => {
        const profiles = getAvailableProfiles();
        const pick = await vscode.window.showQuickPick(profiles, {
            placeHolder: `Current: ${currentProfile}. Select bot profile:`
        });
        if (pick) {
            currentProfile = pick;
            updateStatusBar();
            vscode.window.showInformationMessage(`Hermes active profile switched to: ${currentProfile}`);
        }
    });
    context.subscriptions.push(profileCmd);

    const runTaskCmd = vscode.commands.registerCommand('hermes.runTask', async () => {
        const task = await vscode.window.showInputBox({
            prompt: `Task for Hermes (${currentProfile})`,
            placeHolder: 'e.g. Write a script, analyze architecture, etc.'
        });
        if (!task) return;

        const runnerPath = "C:\\Users\\may\\.gemini\\antigravity-ide\\scratch\\Hermes_Integration\\hermes_acp_runner.py";
        const pythonExe = "F:\\AI\\hermes\\hermes-agent\\venv\\Scripts\\python.exe";
        const cwd = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || process.cwd();

        const terminal = vscode.window.createTerminal(`Hermes ACP: ${currentProfile}`);
        terminal.show();
        terminal.sendText(`& "${pythonExe}" "${runnerPath}" "${task.replace(/"/g, '`"')}" "${cwd}" --profile ${currentProfile}`);
    });
    context.subscriptions.push(runTaskCmd);
}

function deactivate() {
    if (statusBarItem) statusBarItem.dispose();
}

module.exports = { activate, deactivate };
