import os

def getLunarResourcesPath():
    AppdataPath = os.getenv("APPDATA")
    ProgramsPath = AppdataPath + "\\..\\Local\\Programs"
    LunarResourcesPath = ProgramsPath + "\\launcher\\resources"

    return LunarResourcesPath

def backupAsar():
    ResourcePath = getLunarResourcesPath()
    BackupPath = ResourcePath + "\\app.asar.LCM_backup"
    AppPath = ResourcePath + "\\app.asar"

    try:
        file = open(BackupPath)
        if file:
            file.close()
            return "app.asar yedeği zaten var"
    except:
        pass
    
    app = None
    try:
        app = open(AppPath, "rb")
    except Exception as e:
        return "dosyalarda app.asar bulunamadı (lunar client'i yeniden yükleyin?): " + str(e)
    
    try:
        backup = open(BackupPath, "wb")
        backup.write(app.read())
        backup.close()
        app.close()
    except Exception as e:
        return "yedek bulunamadı: " + str(e)
    
    return "başarıyla yedeklendi!"

def restoreBackup():
    ResourcePath = getLunarResourcesPath()
    BackupPath = ResourcePath + "\\app.asar.LCM_backup"
    AppPath = ResourcePath + "\\app.asar"

    app = None
    try:
        app = open(AppPath, "wb")
    except Exception as e:
        return "dosyalarda app.asar bulunamadı (lunar client'i yeniden yükleyin?): " + str(e)
    
    backup = None
    try:
        backup = open(BackupPath, "rb")
    except Exception as e:
        app.close()
        return "yedek bulunamadı: " + str(e)
    
    app.write(backup.read())
    backup.close()
    app.close()
    return "yedek başarıyla geri yüklendi!"

def decompile():
    ResourcePath = getLunarResourcesPath()
    AppPath = ResourcePath + "\\app.asar"
    DecompilePath = ResourcePath + "\\decompiled\\"

    try:
        open(AppPath)
    except Exception as e:
        return "dosyalarda app.asar bulunamadı (lunar client'i yeniden yükleyin?): " + str(e)

    os.system(f"npx asar extract {AppPath} {DecompilePath}")
    return "başarıyla decompile edildi!"

def compile():
    ResourcePath = getLunarResourcesPath()
    AppPath = ResourcePath + "\\app.asar"
    DecompilePath = ResourcePath + "\\decompiled"

    if not os.path.isdir(DecompilePath):
        return "kaynaklarda decompile bulunamadı (decompile'ı çalıştır)"

    os.system(f"npx asar pack {DecompilePath} {AppPath}")
    return "başarıyla compile'landı!"

choices = [
    {
        "Name":"Exit",
        "Desc":"programı kapatır"
    },
    {
        "Name":"BackupAsar",
        "Desc":"app.asar dosyanızı yedekler, böylece bir şey bozulursa orijinalini geri yükleyebilirsin.",
        "Func":backupAsar
    },
    {
        "Name":"RestoreBackup",
        "Desc":"app.asar yedeğinizi geri yükleyerek uygulamayı orijinal durumuna geri yükler.",
        "Func":restoreBackup
    },
    {
        "Name":"Decompile",
        "Desc":"lunar client başlatıcısın içeriğini 'decompiled' adlı bir klasöre çıktı verir.",
        "Func":decompile
    },
    {
        "Name":"Compile",
        "Desc":"decompile edildikten sonra kod içeriğini tekrar bir araya getirir.",
        "Func":compile
    }
]

lastMsg = None

def __main__():
    global lastMsg
    print("")
    print("LunarLauncherDecompiler by yakut")
    print("\n")
    if lastMsg:
        print("Mesaj: " + lastMsg + "\n")

    for index in range(1, len(choices) + 1):
        choice = choices[index - 1]

        print(f"[{index}] {choice.get('Name')}: {choice.get('Desc')}")

    inp = input()
    try:
        inp = int(inp)
    except Exception as e:
        lastMsg = "seçim sayıya dönüştürülemedi: " + str(e)
        __main__()
        return

    chosen = None
    for index in range(1, len(choices) + 1):
        choice = choices[index - 1]

        if inp == index:
            chosen = choice
            break
    
    if not chosen:
        lastMsg = "geçersiz seçim!"
        __main__()
        return
    
    if chosen == choices[0]:
        return

    try:
        lastMsg = chosen.get("Func")()
    except Exception as e:
        lastMsg = "seçim çalıştırılamadı: " + str(e)
    
    __main__()

if __name__ == "__main__":
    __main__()
