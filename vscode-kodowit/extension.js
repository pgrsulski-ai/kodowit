const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const words = require('./words.json');
function activate(context) {
  const output = vscode.window.createOutputChannel('KODOWIT');
  context.subscriptions.push(output);
  async function run(check) {
    if (!vscode.workspace.isTrusted) return vscode.window.showWarningMessage('KODOWIT wymaga zaufanego obszaru roboczego.');
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'kodowit' || editor.document.uri.scheme !== 'file') return vscode.window.showWarningMessage('Otwórz zapisany plik .kodowit.');
    if (editor.document.isDirty && !(await editor.document.save())) return;
    const config = vscode.workspace.getConfiguration('kodowit');
    const core = config.get('corePath') || path.join(__dirname, '..', 'core', 'kodowit.py');
    if (!path.isAbsolute(core) || !fs.existsSync(core)) return vscode.window.showErrorMessage('Ustaw kodowit.corePath na pełną ścieżkę do core/kodowit.py.');
    const file = editor.document.fileName;
    const task = new vscode.Task({type:'kodowit',check}, vscode.TaskScope.Workspace, check?'Sprawdź składnię':'Uruchom program', 'KODOWIT', new vscode.ProcessExecution(config.get('python','python'), ['-X','utf8',core,...(check?['--sprawdz']:[]),file],{cwd:path.dirname(file)}));
    try { await vscode.tasks.executeTask(task); } catch(e) { output.appendLine(String(e)); output.show(); }
  }
  context.subscriptions.push(vscode.commands.registerCommand('kodowit.run',()=>run(false)),vscode.commands.registerCommand('kodowit.check',()=>run(true)),vscode.languages.registerCompletionItemProvider('kodowit',{provideCompletionItems(){return Object.entries(words).flatMap(([kind,items])=>items.map(word=>new vscode.CompletionItem(word,kind==='functions'?vscode.CompletionItemKind.Function:kind==='constants'?vscode.CompletionItemKind.Constant:vscode.CompletionItemKind.Keyword)));}}));
}
module.exports={activate};
