"""This script is used to bump the version of the package. Cargo.toml is used to store the version."""
import toml

def read_version():
    with open("./Cargo.toml", "r") as file:
        data = toml.load(file)
    return data["package"]["version"]

def read_takeoff_client_version():
    with open("../takeoff-client/python-client/pyproject.toml", "r") as file:
        data = toml.load(file)
    return data["project"]["version"]

def write_version(new_version):
    # Read the content of the file
    with open("./Cargo.toml", "r") as file:
        content = file.readlines()

    # Find and update the version line
    for i, line in enumerate(content):
        if line.startswith("version = "):
            content[i] = f'version = "{new_version}"\n'
            break

    # Write the updated content back to the file
    with open("./Cargo.toml", "w") as file:
        file.writelines(content)
    
    # Update version takeoff-gateway version uses
    # Read the content of the file
    with open("../takeoff-gateway/Cargo.toml", "r") as file:
        content = toml.load(file)

    # Find and update the takeoff-config line
    content["dependencies"]["takeoff-config"] = { "version": new_version, "path": "../takeoff-config" }

    # Write the updated content back to the file
    with open("../takeoff-gateway/Cargo.toml", "w") as file:
        toml.dump(content, file)


if __name__ == "__main__":
    new_version = read_takeoff_client_version()
    write_version(new_version)
    print(f"Version updated to: {new_version}")
