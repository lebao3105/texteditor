#!/bin/sh

# Clean
if [[ $1 == "clean" ]]
then
    rm -f *.AppImage
    rm -f ../texteditor/*.AppImage
    rm -f ../texteditor/AppRun
    rm -f ../texteditor/.DirIcon ../texteditor/icon.png
    rm -f ../texteditor/org.lebao3105*
    rm -rf ../texteditor/po
# Or build
elif [[ $1 == "build" ]]
then
    $0 clean # Clean first
    export ARCH=$(uname -m)
    # Dev build
    cp ../data/org.lebao3105.texteditor.Devel.png ../texteditor/
    cp ../data/org.lebao3105.texteditor.desktop ../texteditor/
    cp -r ../po ../texteditor/po
    touch ../texteditor/AppRun
    cat <<EOF > ../texteditor/AppRun
#!/bin/sh
python3 main.py $@
EOF
    chmod +x ../texteditor/AppRun

    # Get appimagetool
    curl -L -o appimagetool-$ARCH.AppImage https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-$ARCH.AppImage
    chmod a+x appimagetool-$ARCH.AppImage

    ## Now just move files ^_^
    mv appimagetool-$ARCH.AppImage ../texteditor
    cd ../texteditor && ./appimagetool-$ARCH.AppImage .
    chmod a+x ./texteditor-$ARCH.AppImage
    mv ./texteditor-$ARCH.AppImage ../makerelease

    ## When everything is done, go back to makerelease
    cd ../makerelease
    echo "All done - use clean parameter to remove all created files"
    echo "You must run this in other directory not this yet."
fi