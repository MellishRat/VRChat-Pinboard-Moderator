# VRChat Pinboard Moderator

A desktop moderation tool for owners and administrators of the Memo Bulletin Board VRChat asset.

This utility allows pinboard owners to view notes, search content, group posts by user hash, and quickly remove unwanted messages without needing to manually inspect the board in VRChat.

---

## Features

* Fetch notes directly from a Pinboard ID
* Search and filter note content
* Group notes by User Hash
* Delete individual notes
* Delete all notes from a selected User Hash
* Highlight potentially problematic content
* Customisable flagged words and URL filters
* Standalone Windows executable available
* Open source Python source code included

---

## Flagged Words Configuration

The application uses a file called:

```text
flagged_words.json
```

This file controls which words, phrases, and URL fragments are highlighted by the moderator tool.

Examples include:

* Profanity
* Hate speech
* Harassment
* URL spam
* Advertising links

You can freely edit this file to suit your own community, language, or moderation requirements.

The application can reload the configuration without requiring changes to the source code.

### Important

The flagged words system:

* Does NOT block posts
* Does NOT delete posts automatically
* Does NOT modify the original pinboard

It only highlights notes locally inside the moderation tool.

---

## Requirements

To use this application you must have:

* Pinboard ID
* Hash Key

The Hash Key is required for note deletion functions.

---

## How To Use

1. Launch the application.
2. Enter the Pinboard ID.
3. Enter the Hash Key.
4. Click **Fetch Notes**.
5. Review notes and user groups.
6. Use the search function to locate content.
7. Delete individual notes or remove all notes from a selected user hash.
8. Optionally customise `flagged_words.json`.

---

## Downloads

Pre-built Windows executables can be found in the GitHub Releases section.

Alternatively, you can run the Python source directly.

---

## Building From Source

Requirements:

* Python 3.10 or newer
* PyInstaller

Build:

```bash
py -m PyInstaller pinboard_moderator_gui.spec --clean
```

The executable will be generated in:

```text
dist/VRChat_Pinboard_Moderator.exe
```

---

## Disclaimer

This project is an unofficial third-party moderation utility.

It is not affiliated with, endorsed by, or supported by the original creator.

This tool is intended only for moderation and administration of pinboards that you own or manage.

---

## Original Asset

This utility was created for use with:

Memo Bulletin Board for VRChat

Creator:
Oikki

Booth Page:

https://oikki.booth.pm/items/5950794

If you find this utility useful, please consider supporting the original creator by purchasing their asset.

---

## Special Thanks

Special thanks to Oikki for creating Memo Bulletin Board and for kindly allowing this moderation utility to be shared publicly.

---

## License

This repository contains only the moderation utility.

No source code, assets, models, textures, shaders, or proprietary content from the original Memo Bulletin Board package are included.

Please obtain the original asset from the creator if you wish to use Memo Bulletin Board in your own VRChat worlds.


# VRChat Pinboard Moderator

Memo Bulletin Board 用の管理者向けデスクトップモデレーションツールです。

VRChatワールド内で直接ボードを確認することなく、投稿の確認・検索・削除を行うことができます。

---

## 主な機能

* Pinboard IDから投稿を取得
* 投稿内容の検索・フィルタリング
* User Hashごとのグループ表示
* 個別投稿の削除
* 特定User Hashの投稿を一括削除
* 問題のある可能性がある投稿のハイライト表示
* カスタマイズ可能なフラグワード機能
* Windows向け実行ファイル（EXE）を提供
* Pythonソースコードを公開

---

## フラグワード設定

本ツールは以下のファイルを使用します。

```text
flagged_words.json
```

このファイルでは、ハイライト対象となる単語・フレーズ・URLを自由に設定できます。

例：

* 不適切な表現
* 差別的表現
* 嫌がらせ
* URLスパム
* 広告リンク

コミュニティや言語に合わせて自由に編集できます。

### 注意

フラグワード機能は、

* 投稿をブロックしません
* 自動削除を行いません
* ピンボードの内容を書き換えません

管理ツール内でハイライト表示するためだけの機能です。

---

## 必要なもの

利用には以下が必要です。

* Pinboard ID
* Hash Key

投稿削除機能には Hash Key が必要です。

---

## 使い方

1. アプリケーションを起動します。
2. Pinboard ID を入力します。
3. Hash Key を入力します。
4. 「Fetch Notes」をクリックします。
5. 投稿内容を確認します。
6. 検索機能で投稿を絞り込みます。
7. 必要に応じて投稿を削除します。
8. `flagged_words.json` を編集して独自のルールを設定できます。

---

## ダウンロード

Windows向け実行ファイルは GitHub Releases からダウンロードできます。

Pythonソースコードから直接実行することも可能です。

---

## ソースからビルド

必要環境：

* Python 3.10以降
* PyInstaller

ビルドコマンド：

```bash
py -m PyInstaller pinboard_moderator_gui.spec --clean
```

生成される実行ファイル：

```text
dist/VRChat_Pinboard_Moderator.exe
```

---

## 免責事項

本ツールは非公式のサードパーティ製ユーティリティです。

作者様による公式サポート対象ではありません。

自身が所有または管理するピンボードの管理用途のみを目的としています。

---

## 元アセット

本ツールは以下のアセット向けに開発されました。

Memo Bulletin Board for VRChat

作者：
Oikki

Boothページ：

https://oikki.booth.pm/items/5950794

本ツールが役に立った場合は、ぜひ元アセットの購入や作者様への応援をご検討ください。

---

## 謝辞

Memo Bulletin Board を制作し、本ツールの公開を快く許可してくださった Oikki 様に感謝いたします。

---

## ライセンス

このリポジトリにはモデレーションツールのみが含まれています。

Memo Bulletin Board 本体のソースコード、アセット、モデル、テクスチャ、シェーダー等は含まれていません。

Memo Bulletin Board を利用する場合は、必ず作者様から正規に入手してください。
