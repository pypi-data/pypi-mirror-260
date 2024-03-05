import os
import shutil

import setuptools


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # 定义要清理的目录和文件类型
        dirs_to_remove = ['./build', './dist', './*.egg-info']

        # 删除目录
        for dir_path in dirs_to_remove:
            print(f"Removing directory: {dir_path}")
            shutil.rmtree(dir_path, ignore_errors=True)

        # 删除文件
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.pyc') or file.endswith('.tgz'):
                    file_path = os.path.join(root, file)
                    print(f"Removing file: {file_path}")
                    os.remove(file_path)

            # 删除 __pycache__ 目录
            for dir in dirs:
                if dir == "__pycache__":
                    dir_path = os.path.join(root, dir)
                    print(f"Removing directory: {dir_path}")
                    shutil.rmtree(dir_path, ignore_errors=True)

        print("Cleaned up.")


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as rfr:
    required = rfr.read().splitlines()

setuptools.setup(
    name="xiaolu_tool",
    version="0.0.5",
    author="xiaolu-developer",
    author_email="jiaboyu@xiaoluyy.com",
    description="A tool for xiaolu data server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject"   内部项目不需要加url,
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    cmdclass={"clean": CleanCommand},
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
