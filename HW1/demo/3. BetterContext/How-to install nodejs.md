# How to Install Node.js for Development using nvm

This guide explains the best-practice method for installing Node.js in a development environment, particularly on Linux or WSL (Windows Subsystem for Linux).

## The Problem: System Package Managers (`apt`) are Outdated

When you need Node.js for a development tool like Playwright, a common first step is to use the system's package manager:

```bash
# This method is NOT recommended for development
sudo apt install nodejs npm
```

**The issue with this approach is that `apt` often provides a very old version of Node.js.** In our case, it installed Node.js v12, but modern tools require much newer versions (e.g., v18+). This leads to incompatibility errors.

## The Solution: Use `nvm` (Node Version Manager)

The industry-standard solution is to use **`nvm`**, a tool that lets you manage multiple Node.js versions on a per-user basis, without requiring administrative (`sudo`) privileges for day-to-day use.

### Step 1: Remove Any Existing System-Wide Node.js

First, ensure a clean slate by purging any versions installed via `apt`.

```bash
sudo apt remove --purge nodejs npm
sudo apt autoremove
```

### Step 2: Install `nvm`

Next, install the `nvm` tool itself. This command downloads and runs the official installation script.

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```
*Note: This does **not** install Node.js, only the manager.* You may need to close and reopen your terminal after this step for the `nvm` command to become available.

### Step 3: Install Node.js using `nvm`

Now, use `nvm` to install the latest **LTS (Long-Term Support)** version of Node.js. This is the recommended, stable version for most projects.

```bash
nvm install --lts
```

`nvm` will download, install, and automatically start using the latest LTS version.

### Step 4: Verify the Installation

Check that the correct versions are now active.

```bash
node --version
# Expected output: v22.20.0 (or the latest LTS version)

npm --version
# Expected output: 10.9.3 (or similar)
```

## Why `nvm` is Better than `apt` for Development

| Feature | `sudo apt` (System-wide) | `nvm` (User-level) |
| :--- | :--- | :--- |
| **Privileges** | Requires `sudo` for installation and global packages. | **No `sudo` needed** for managing Node or packages. Safer and more convenient. |
| **Versions** | Installs one, often outdated, system-wide version. | **Manages multiple versions.** Easily switch with `nvm use 18`, `nvm use 22`, etc. |
| **Flexibility**| Can cause conflicts if different projects need different Node versions. | Perfect for managing per-project version requirements. |
| **Updates** | Slow to receive new Node.js releases. | Get the **latest Node.js versions** as soon as they are released. |

By following these steps, you have a robust, flexible, and modern Node.js development environment.
