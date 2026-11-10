// Zengő indító: a hordozható mappa venvjeit a mappa mostani helyéhez igazítja, majd konzolablak nélkül
// elindítja az asztali appot. Fordítás: scripts\build_portable.ps1 (a Windowsba épített csc.exe-vel).
using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;

static class Zengo
{
    const string Title = "Zengő";

    [STAThread]
    static int Main()
    {
        string root = AppDomain.CurrentDomain.BaseDirectory.TrimEnd('\\');
        try
        {
            foreach (string venv in new[] { ".venv", @"engines\f5\.venv", @"engines\piper\.venv" })
                FixVenv(root, Path.Combine(root, venv));
            string pythonw = Path.Combine(root, @".venv\Scripts\pythonw.exe");
            if (!File.Exists(pythonw))
                throw new FileNotFoundException("Hiányzik a Python környezet: " + pythonw);
            var psi = new ProcessStartInfo(pythonw, "-m app.desktop --root \"" + root + "\"")
            {
                WorkingDirectory = root,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            Process.Start(psi);
            return 0;
        }
        catch (Exception e)
        {
            MessageBox.Show("A Zengő nem indult el:\n\n" + e.Message, Title, MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 1;
        }
    }

    // A venv a pyvenv.cfg "home" sorában abszolút úton hivatkozik a Pythonra; ezt a runtime\pyXY mappára állítjuk.
    static void FixVenv(string root, string venv)
    {
        string cfg = Path.Combine(venv, "pyvenv.cfg");
        if (!File.Exists(cfg)) return;
        string[] lines = File.ReadAllLines(cfg, Encoding.UTF8);
        string ver = lines.Select(l => l.Split(new[] { '=' }, 2))
                          .Where(p => p.Length == 2 && p[0].Trim() == "version_info")
                          .Select(p => p[1].Trim()).FirstOrDefault() ?? "";
        string[] parts = ver.Split('.');
        if (parts.Length < 2) return;
        string home = Path.Combine(root, @"runtime\py" + parts[0] + parts[1]);
        bool changed = false;
        for (int i = 0; i < lines.Length; i++)
        {
            if (lines[i].TrimStart().StartsWith("home") && lines[i].Contains("="))
            {
                string want = "home = " + home;
                if (lines[i] != want) { lines[i] = want; changed = true; }
            }
        }
        if (changed) File.WriteAllLines(cfg, lines, new UTF8Encoding(false));
    }
}
