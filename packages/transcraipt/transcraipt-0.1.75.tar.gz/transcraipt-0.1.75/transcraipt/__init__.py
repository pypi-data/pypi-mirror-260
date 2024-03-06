import os

def run_post_install_scripts():
    # Check if the post-install script has already been executed
    flag_file = os.path.join(os.path.dirname(__file__), '.post_install_done')
    if os.path.exists(flag_file):
        return

    # ASCII Art Message
    ascii_art_message = """
    ****************************************************
    *    Installation Successful!                      *
    *    To enable autocomplete, please run:           *
    ****************************************************
    """
    print(ascii_art_message)

    # Instructions for bash and zsh
    bash_instructions = "For bash users:\n" + "echo 'eval \"$(register-python-argcomplete transcribe-audio)\"' >> ~/.bashrc\n"
    zsh_instructions = "For zsh users:\n" + "echo 'eval \"$(register-python-argcomplete transcribe-audio)\"' >> ~/.zshrc\n"
    print(bash_instructions)
    print(zsh_instructions)

    # Instructions for Windows PowerShell
    if os.name == 'nt':
        powershell_instructions = "For PowerShell users:\n" + "Add the following line to your PowerShell profile file:\n" + "Invoke-Expression -Command $(register-python-argcomplete transcribe-audio)\n"
        print(powershell_instructions)

    reminder_message = """
    ****************************************************
    *    Don't forget to restart your terminal!        *
    ****************************************************
    """
    print(reminder_message)

    # Create a flag file to indicate the post-install script has been executed
    with open(flag_file, 'w') as f:
        f.write('')

# Execute the post-install scripts the first time this module is imported
run_post_install_scripts()