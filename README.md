> [!CAUTION]
> The only other official source to get MultiBlox from is [vercel-multiblox.vercel.app](https://vercel-multiblox.vercel.app)!

# <img src="https://github.com/DraxFM/MultiBlox/raw/main/md/icon.png" width="48"/> MultiBlox v1.0.4

MultiBlox is an open source software written in Python that lets you run multiple instances of Roblox.  
I have decided to make this after pizzaboxer removed multi instance launching from Bloxstrap, originally not planning to make it public.  

![image](https://github.com/user-attachments/assets/c73d44db-a74d-4fb0-8e6c-4d7d9e3bc01e)


Compatible with Windows 10/11, untested on MacOS/Linux.

## :large_blue_circle: - Content
- [Supported Bootstrappers](#bootstrapper)
- [:toolbox: - Usage](#usage)
- [Read before Using](#usage2)
- [FAQ](#faq)
- [:wave: - Authors](#authors)
- [:exclamation: - License](#license)

---

### <a id="bootstrapper"></a> Supported Bootstrappers
- ### Roblox Default Bootstrapper
  #### This is the default Roblox Bootstrapper that gets installed when obtaining Roblox through its [official](https://www.roblox.com/download) website.
- ### Bloxstrap
  #### This is a custom community made Bootstrapper made by [pizzaboxer](https://www.github.com/pizzaboxer). You can get it [here](https://bloxstraplabs.com).

---

### <a id="usage"></a> :toolbox: - Usage

1. Install the [latest release](https://github.com/DraxFM/MultiBlox/releases/latest)
2. Extract the .zip folder
3. Run **MultiBlox.exe**
4. Make sure to go into settings and select your desired Roblox Bootstrapper!
5. Only then press "**Toggle MultiBlox**"
6. The program will do the rest

---

### <a id="usage2"></a> Read before Using

Do you get the popup "Windows Defender SmartScreen prevented an unrecognized app from starting"? Read the [respective FAQ article](#faq) for more information.

Usually MultiBlox automatically closes any Roblox instance when toggling the feature, but in any case it doesn't just close all Roblox applications manually.
You can use "Start Roblox Instance" if you want but you can also just launch from your Start Menu or via your browser.
"Kill Roblox Instances" is not particularly for MultiBlox, as MultiBlox won't freeze or slow Roblox down, I just find it useful when running into problems and as I use MultiBlox myself it's there.

---

### <a id="faq"></a> FAQ
#### Windows Defender SmartScreen prevented an unrecognized app from starting
This has a very high chance of happening. This does not happen because Windows Defender thinks that the file is a virus, this happens because I do not have a signing certificate. I could self-sign but this will not mitigate the popup. The only way to properly remove the popup is by obtaining either an EV or OV certificate. EV certs base out at 500$ - 700$ a year while OV certs are cheaper at 100$ - 500$ a year. Well of course I can't afford this. The only other way to remove the popup is by gaining reputation by people installing and running the software. This can take months and requires thousands of users to run the application. The whole process is reset when updating the application to a new version. I'll likely never be able to remove this.

---

#### How can I trust MultiBlox?
It's open source. That means you can read the raw code I wrote to make this. You could even run the raw python file but this would require you to install several libraries and Python itself. MultiBlox is packaged using vanilla pyinstaller with **noconsole, onefile, icon** args. You can decompile MultiBlox, it is not obfuscated.

---

#### Can I get banned for using this?
In terms of getting banned by Roblox Anti-Cheat you will not get banned. This software does not inject into Roblox, it does not touch Roblox's internals in any way. Though, always remember to follow the rules of the different Roblox Experiences. Some Experiences do not allow Alt farming etc. which is made possible with this software. If someone catches you alt farming or abusing this software in a way that it breaks rules, you have the chance of getting banned from this experience. I am not liable for what YOU do with this software!

---

#### How does it work?  
Roblox mobilises **handles** to ensure that it only runs once. It creates this handle upon running Roblox.  
MultiBlox will close all current Roblox processes, it will then run a thread that will create a handle to a **mutex**. It will "inherit" the handle that Roblox will try to create when launching, but it won't be able to as it can't access a foreign thread and just     close this mutex. You will be able to open as many Roblox instances as you want, just remember that they take up RAM so your PC will get slower per Roblox Instance.

---


## <a id="authors"></a> :wave: - Authors

* [**Drax**](https://github.com/DraxFM) - *Inital Work*

**Discord: [draxfm](https://discord.com/users/654343206275907585)**

Need help? Join the [**Discord**](https://discord.gg/sEXECdC3Et)!

## <a id="license"></a> :exclamation: - License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
