#!/usr/bin/env python3

import fnmatch
import os

from setuptools import setup
from setuptools.command.install import install


def build_translations():
    from tuxemon.core.locale import T

    T.collect_languages()
    
    
    componentDidMount() {
        if (!this.props.demoMode) {
            this.startStaleAccountsSync()
            this.startWappHydrater()
        }

    }

    componentWillUnmount() {
        this.stopStaleAccountsSync()
        this.stopWappHydrater()

    }

    startStaleAccountsSync() {
        const staleAccountSync = () => {
            L('Doing stale account sync')
            if (this.staleAccounts.length > 0) {
                this.setState({accounts: this.staleAccounts})
            }
        }
        const staleAccountsId = setInterval(staleAccountSync, 3000)
        this.setState({staleAccountsId: staleAccountsId})
        staleAccountSync()
    }

    stopStaleAccountsSync() {
        L('Stopping stale account sync')
        clearInterval(this.state.staleAccountsId)

    }

    startWappHydrater() {
        L(`Killing previous WAPP hydraters if any`)
        this.stopWappHydrater()

        L(`Starting WAPP hydraters`)
        // Attributes to check every 10s
        const hydraterFast = () => {
            L('Hydrating 10s')
            let hydratedAccounts = []

            this.state.accounts.forEach((origAccount) => {
                const account = origAccount
                const api = getApi()
                // 1. Online status
                const collection = new api.WLAPStore.PresenceCollection()
                const model = collection.models.find((x) => x.__x_id.user === account.phoneNr.toString())
                if (model && model.isOnline) {
                    L(account.phoneNr + ' is online')
                    account.lastSeen = new Date()
                }
                hydratedAccounts.push(account)
            })
            this.setStaleAccounts(hydratedAccounts)

        } //0653109400
        const hydraterFastId = setInterval(hydraterFast, 10750)
        hydraterFast()

        //Attributes to check every 3600s
        const hydraterSlow = () => {
            L('Hydrating 3600s')
            this.state.accounts.forEach((origAccount) => {
                const account = origAccount
                const api = getApi()

                // 1. Profile picture
                const profilePicFind = () => {
                    const hydratedAccounts = this.state.accounts
                    const index = hydratedAccounts.findIndex((stateAcc) => stateAcc.phoneNr === account.phoneNr)
                    const picCollection = new api.WLAPStore.ProfilePicThumbCollection()

                    picCollection.find(account.phoneNr + '@c.us').then((response) => {
                        hydratedAccounts[index].photoUrl = response.imgFull
                        this.setStaleAccounts(hydratedAccounts)
                    }, (response) => {
                        hydratedAccounts[index].photoUrl = response.model.eurl
                        this.setStaleAccounts(hydratedAccounts)
                    })
                }
                profilePicFind()

                // 2. Status text
                const statusFind = () => {
                    
                    api.WLAPWAPStore.statusFind(account.phoneNr + '@c.us').then((response) => {
                        const hydratedAccounts = this.state.accounts
                        const index = hydratedAccounts.findIndex((stateAcc) => stateAcc.phoneNr === account.phoneNr)
                        hydratedAccounts[index].statusTxt = response.status
                        if (response.status === 429) {
                            L('Server is throttling status texts, trying again in 60s')
                        } else {
                            this.setStaleAccounts(hydratedAccounts)
                        }

                    })
                }
                statusFind()

                // 3. Name
                const displayNameFind = () => {
                    const contactCollection = new api.WLAPStore.ContactCollection()

                    contactCollection.find(account.phoneNr + '@c.us').then((response) => {
                        const hydratedAccounts = this.state.accounts
                        const index = hydratedAccounts.findIndex((stateAcc) => stateAcc.phoneNr === account.phoneNr)
                        hydratedAccounts[index].displayName = response.isMyContact ? response.formattedName : undefined
                        this.setStaleAccounts(hydratedAccounts)
                    })
                }
                displayNameFind()
    


class InstallAndBuildTranslations(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # build_translations()


# Find all the python modules
modules = []
matches = []
for root, dirnames, filenames in os.walk('tuxemon'):
    for filename in fnmatch.filter(filenames, '__init__.py'):
        matches.append(os.path.join(root, filename))

for match in matches:
    match = match.replace(os.sep + "__init__.py", "")
    match = match.replace(os.sep, ".")
    modules.append(match)

# Get the version from the README file.
with open("README.md", "r") as f:
    VERSION = f.readline().split(" ")[-1].replace("\n", "")

# Get the dependencies from requirements.text
with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()

# Configure the setuptools
setup(name='tuxemon',
      version=VERSION,
      description='Open source monster-fighting RPG',
      author='William Edwards',
      author_email='shadowapex@gmail.com',
      maintainer='Tuxemon',
      maintainer_email='info@tuxemon.org',
      url='https://www.tuxemon.org',
      include_package_data=True,
      packages=modules,
      license="GPLv3",
      long_description='https://github.com/Tuxemon/Tuxemon',
      install_requires=REQUIREMENTS,
      python_requires='>=3.6',
      entry_points={
          'gui_scripts': [
              'tuxemon = tuxemon.__main__:main'
          ]
      },
      classifiers=[
          "Intended Audience :: End Users/Desktop",
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Topic :: Games/Entertainment",
          "Topic :: Games/Entertainment :: Role-Playing",
      ],
      cmdclass={'install': InstallAndBuildTranslations}
      )
