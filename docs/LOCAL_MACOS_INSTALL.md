# Zenith Local — installation personnelle macOS

Le lanceur commun **0.1.1** compile puis prépare **`Zenith Local.app`**, identifiant
**`com.arn-lab.zenith.local`**. Cette édition s'installe à côté du **`Zenith.app`** du
cask, qui reste géré par Homebrew. Le composant refuse d'écraser une cible Homebrew.
Il ne désinstalle rien, ne corrige pas l'ancienne application et ne désactive pas Gatekeeper.
Les sources Swift, le build et les archives publics sont inchangés.

## Prérequis et dépendance source épinglée

macOS 14+, Swift 5.9+/Xcode Command Line Tools et Python avec pip et filtres tarfile
sécurisés (3.10.12+, 3.11.4+ ou 3.12+). Le composant standard library vit dans
`ArN-LaB/homebrew-tap/developer-tools/macos-local-installer`.
Sa référence prévue est `local-installer-v0.1.1` : publication requise avant les
intégrations clientes, non annoncée comme disponible pendant la revue.

La dépendance `ArN-LaB/vpn-tools` est épinglée au commit publié de `main`
**`dbaeffb7e4adb5dccf5ae4fae9d3d763e9d4bcad`**. Le build refuse un autre HEAD ou un
arbre sale avant de créer son workspace ; il ne change jamais une branche existante.
Préparer un checkout dédié, hors des dossiers synchronisés si possible :

```sh
# Ces commandes créent un NOUVEAU clone ; ne pas réutiliser un dossier de travail actif.
git clone --single-branch --branch main git@github.com:ArN-LaB/vpn-tools.git \
  "$HOME/Library/Application Support/ArN-LaB Local Installer/sources/vpn-tools-dbaeffb7"
git -C "$HOME/Library/Application Support/ArN-LaB Local Installer/sources/vpn-tools-dbaeffb7" \
  checkout --detach dbaeffb7e4adb5dccf5ae4fae9d3d763e9d4bcad
```

Le chemin ci-dessus est celui du manifeste. Pour un autre emplacement :

```sh
export VPN_TOOLS_SRC="/chemin/du/checkout-epingle"
export ARNLAB_INSTALLER_ROOT="/chemin/homebrew-tap/developer-tools/macos-local-installer"
./install-local.command --dry-run
./install-local.command --build-only
./install-local.command --build --simulate
./install-local.command
```

Le double-clic ouvre le parcours interactif. `ARNLAB_PYTHON` choisit un interpréteur
précis. Version et SHA-256 du moteur sont vérifiés avant exécution. Aucun téléchargement
automatique du composant. Le lanceur conserve l'entrée Terminal pour les confirmations.

## Build isolé et signature

Les sources propres de Zenith et de vpn-tools sont exportées dans un dossier privé.
`build_app.sh` s'exécute dans cet export ; il ne supprime pas le `.app` du checkout.
Le bundle neuf, produit comme `Zenith.app`, reçoit son nom et son identifiant locaux,
puis son sceau ad hoc. Seule la signature provisoire du linker peut être finalisée ;
un bundle déjà scellé ou portant une autre signature n'est jamais re-signé pour changer
son identité. Le reçu est établi sur les octets finaux vérifiés.

Pip récupère les dépendances comme auparavant. Elles restent non verrouillées : le
reçu décrit les octets obtenus, pas une reproductibilité binaire. Le runtime Python
reste nécessaire à l'exécution : sources et bibliothèques sont embarquées, pas Python.
Aucun test VPN n'est déclenché par le composant.

## Installer, sauvegarder, restaurer

Le build affiche le chemin du bundle et un reçu UUID privé, créé sur ce Mac :

```sh
./install-local.command --app /chemin/Zenith.app --receipt UUID_DU_RECU
./install-local.command --list-backups
./install-local.command --rollback UUID_DE_TRANSACTION
```

Le chemin de build peut porter le nom `Zenith.app` ; la destination est toujours
`/Applications/Zenith Local.app`, avec son identifiant distinct contrôlé dans le reçu.
Quitter normalement l'édition cible avant remplacement/restauration. Le moteur refuse
une cible encore active et ne tue aucun processus. Il ne lance pas l'application.

L'installation exige `INSTALLER`, la restauration `RESTAURER`. Un retrait de quarantaine
éventuel exige séparément `RETIRER` sur la copie préparée seulement. Le bundle source
reste intact. Un artefact téléchargé sans reçu local correspondant est refusé.

La version locale précédente est conservée dans
`/Applications/.arnlab-local-installer/UUID/previous.app`. Le retour arrière contrôle
les empreintes et identités ; toute cible reprise par Homebrew ou modifiée est refusée.
`--list-backups` affiche tailles et états, y compris les préparations interrompues.
Aucune purge automatique ; examiner les copies avant tout nettoyage manuel.

## Cohabitation et limites

Les préférences liées au bundle ont un domaine local distinct ; aucun réglage ou secret
n'est migré automatiquement. Les sources Zenith partagent encore
`~/Library/Application Support/VPN Tools/runtime` entre les éditions : **ne pas les
lancer simultanément pour un travail VPN**. L'installeur ne change ni ce runtime, ni
Mullvad, ni les paramètres réseau. La cohabitation protège les bundles du cask et du
build local ; elle ne promet pas une isolation complète des données d'exécution.

Le [contrat commun](https://github.com/ArN-LaB/homebrew-tap/tree/main/developer-tools/macos-local-installer)
détaille les garanties et limites. Le guide sera disponible après intégration sur main ;
le manifeste épingle la référence versionnée. Une signature ad hoc et un reçu ne
constituent pas une notarisation Apple. Les lancements réels restent une recette séparée.
