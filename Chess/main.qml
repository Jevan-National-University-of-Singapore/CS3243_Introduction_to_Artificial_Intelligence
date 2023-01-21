import QtQuick 2.7
import QtQuick.Controls 2.15
import QtQuick.Window 2.2
import FileIO 1.0



ApplicationWindow {
    id: root

    visible: true
    width: Screen.width/1.5
    height: Screen.height/1.5
    color: "black"

    property string chessboard_state
    property int row: 8
    property int column: 8
    property string k: kInput.text

    function intToChar(n) {
        var ordA = 'a'.charCodeAt(0);
        var ordZ = 'z'.charCodeAt(0);
        var len = ordZ - ordA + 1;

        var s = "";
        while(n >= 0) {
            s = String.fromCharCode(n % len + ordA) + s;
            n = Math.floor(n / len) - 1;
        }
        return s;
    }

    MouseArea{
        anchors.fill: parent
        onClicked: {
            console.log("test")
            focusItem.forceActiveFocus()
        }
    }


    FileIO{
        id: textFile
        source: "testing.txt"
    }

    Rectangle {
        id: pieceSelection
        width: root.width/4
        height: root.height
        color: "grey"
        radius: 5
        border{
            width:2
            color: "white"
        }
        anchors{
            right: parent.right
            top: parent.top
        }

        Rectangle {
            id: kingPiece
            height: width
            width: pieceSelection.width/3
            color: "transparent"
            anchors {
                top: pieceSelection.top
                left: pieceSelection.left
                leftMargin: width/50
                topMargin: height/50
            }
            Image {
                id: kingPieceIcon
                anchors.fill: kingPiece
                source: "qrc:/Images/King.png"
                fillMode: Image.PreserveAspectFit
                autoTransform: true
            }
        }
        Rectangle {
            id: queenPiece
            height: kingPiece.height
            width: height
            color: "transparent"
            anchors {
                top: pieceSelection.top
                left: kingPiece.right
                leftMargin: width/50
                topMargin: height/50
            }
            Image {
                id: queenPieceIcon
                anchors.fill: queenPiece
                source: "qrc:/Images/Queen.png"
                fillMode: Image.PreserveAspectFit
                autoTransform: true
            }
        }
        Rectangle {
            id: bishopPiece
            height: kingPiece.height
            width: height
            color: "transparent"
            anchors {
                top: kingPiece.bottom
                left: kingPiece.left
                topMargin: height/50
            }
            Image {
                id: bishopPieceIcon
                anchors.fill: bishopPiece
                source: "qrc:/Images/Bishop.png"
                fillMode: Image.PreserveAspectFit
                autoTransform: true
            }
        }
        Rectangle {
            id: rookPiece
            height: kingPiece.height
            width: height
            color: "transparent"
            anchors {
                top: queenPiece.bottom
                right: queenPiece.right
                topMargin: height/50
            }
            Image {
                id: rookPieceIcon
                anchors.fill: rookPiece
                source: "qrc:/Images/Rook.png"
                fillMode: Image.PreserveAspectFit
                autoTransform: true
            }
        }
        Rectangle {
            id: knightPiece
            height: kingPiece.height
            width: height
            color: "transparent"
            anchors {
                top: bishopPiece.bottom
                left: kingPiece.left
                topMargin: height/50
            }
            Image {
                id: knightPieceIcon
                anchors.fill: knightPiece
                source: "qrc:/Images/Knight.png"
                fillMode: Image.PreserveAspectFit
                autoTransform: true
            }
        }

    }

    ListModel {
        id: columnModel
    }
    Item {
        id: focusItem
        focus: true
        Keys.onPressed: {
                switch(event.text){
                    case "k":
                        for (var i = 0; i < columnModel.count; i++){
                            var row_pieces = JSON.parse(columnModel.get(i).row_pieces)
                            var all_selected = JSON.parse(columnModel.get(i).square_selected)
                            var row_state = JSON.parse(columnModel.get(i).row_state)
                            for (var square = 0; square < all_selected.length; square++){
                                if (all_selected[square] === true){
                                    row_pieces[square] = "king"
                                    row_state[square] = "qrc:/Images/King.png"
                                    all_selected[square] = false
                                }
                            }

                            columnModel.setProperty(i, "row_pieces",JSON.stringify(row_pieces))
                            columnModel.setProperty(i,"square_selected", JSON.stringify(all_selected))
                            columnModel.setProperty(i,"row_state", JSON.stringify(row_state))
                        }
                        break
                    case "q":
                        for (var i = 0; i < columnModel.count; i++){
                            var row_pieces = JSON.parse(columnModel.get(i).row_pieces)
                            var all_selected = JSON.parse(columnModel.get(i).square_selected)
                            var row_state = JSON.parse(columnModel.get(i).row_state)
                            for (var square = 0; square < all_selected.length; square++){
                                if (all_selected[square] === true){
                                    row_pieces[square] = "queen"
                                    row_state[square] = "qrc:/Images/Queen.png"
                                    all_selected[square] = false
                                }
                            }

                            columnModel.setProperty(i, "row_pieces",JSON.stringify(row_pieces))
                            columnModel.setProperty(i,"square_selected", JSON.stringify(all_selected))
                            columnModel.setProperty(i,"row_state", JSON.stringify(row_state))
                        }
                        break

                    case "b":
                        for (var i = 0; i < columnModel.count; i++){
                            var row_pieces = JSON.parse(columnModel.get(i).row_pieces)
                            var all_selected = JSON.parse(columnModel.get(i).square_selected)
                            var row_state = JSON.parse(columnModel.get(i).row_state)
                            for (var square = 0; square < all_selected.length; square++){
                                if (all_selected[square] === true){
                                    row_pieces[square] = "bishop"
                                    row_state[square] = "qrc:/Images/Bishop.png"
                                    all_selected[square] = false
                                }
                            }

                            columnModel.setProperty(i, "row_pieces",JSON.stringify(row_pieces))
                            columnModel.setProperty(i,"square_selected", JSON.stringify(all_selected))
                            columnModel.setProperty(i,"row_state", JSON.stringify(row_state))
                        }
                        break
                    case "r":
                        for (var i = 0; i < columnModel.count; i++){
                            var row_pieces = JSON.parse(columnModel.get(i).row_pieces)
                            var all_selected = JSON.parse(columnModel.get(i).square_selected)
                            var row_state = JSON.parse(columnModel.get(i).row_state)
                            for (var square = 0; square < all_selected.length; square++){
                                if (all_selected[square] === true){
                                    row_pieces[square] = "rook"
                                    row_state[square] = "qrc:/Images/Rook.png"
                                    all_selected[square] = false
                                }
                            }

                            columnModel.setProperty(i, "row_pieces",JSON.stringify(row_pieces))
                            columnModel.setProperty(i,"square_selected", JSON.stringify(all_selected))
                            columnModel.setProperty(i,"row_state", JSON.stringify(row_state))
                        }
                        break
                    case "h":
                        for (var i = 0; i < columnModel.count; i++){
                            var row_pieces = JSON.parse(columnModel.get(i).row_pieces)
                            var all_selected = JSON.parse(columnModel.get(i).square_selected)
                            var row_state = JSON.parse(columnModel.get(i).row_state)
                            for (var square = 0; square < all_selected.length; square++){
                                if (all_selected[square] === true){
                                    row_pieces[square] = "knight"
                                    row_state[square] = "qrc:/Images/Knight.png"
                                    all_selected[square] = false
                                }
                            }

                            columnModel.setProperty(i, "row_pieces",JSON.stringify(row_pieces))
                            columnModel.setProperty(i,"square_selected", JSON.stringify(all_selected))
                            columnModel.setProperty(i,"row_state", JSON.stringify(row_state))
                        }
                        break
                    case "o":
                        for (var i = 0; i < columnModel.count; i++){
                            var row_pieces = JSON.parse(columnModel.get(i).row_pieces)
                            var all_selected = JSON.parse(columnModel.get(i).square_selected)
                            var row_state = JSON.parse(columnModel.get(i).row_state)
                            for (var square = 0; square < all_selected.length; square++){
                                if (all_selected[square] === true){
                                    row_pieces[square] = "obstacle"
                                    row_state[square] = "qrc:/Images/Obstacle.png"
                                    all_selected[square] = false
                                }
                            }

                            columnModel.setProperty(i, "row_pieces",JSON.stringify(row_pieces))
                            columnModel.setProperty(i,"square_selected", JSON.stringify(all_selected))
                            columnModel.setProperty(i,"row_state", JSON.stringify(row_state))
                        }
                        break
                    case "x":
                        for (var i = 0; i < columnModel.count; i++){
                            var row_pieces = JSON.parse(columnModel.get(i).row_pieces)
                            var all_selected = JSON.parse(columnModel.get(i).square_selected)
                            var row_state = JSON.parse(columnModel.get(i).row_state)
                            for (var square = 0; square < all_selected.length; square++){
                                if (all_selected[square] === true){
                                    row_pieces[square] = ""
                                    row_state[square] = ""
                                    all_selected[square] = false
                                }
                            }

                            columnModel.setProperty(i, "row_pieces",JSON.stringify(row_pieces))
                            columnModel.setProperty(i,"square_selected", JSON.stringify(all_selected))
                            columnModel.setProperty(i,"row_state", JSON.stringify(row_state))
                        }
                        break
                    }
            }
    }

    Rectangle{
        id: chessboard
        height: root.height/1.02
        width: height
        color: "transparent"
        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: width/6
        }
        radius: 5

        Column {
            id: column
            anchors.centerIn: chessboard
            Repeater {
                id: column_repeater
                model: columnModel
                Row {
                    id: row
                    property string firstColor: index%2? "#333333":"grey"
                    property string secondColor: index%2? "grey":"#333333"
                    property string firstColorSelected:  index%2? "#113311":"#224022"
                    property string secondColorSelected:  index%2? "#224022":"#113311"
                    property int _y: index
                    property string square_selected: model.square_selected
                    property string row_pieces: model.row_pieces
                    Repeater {
                        id: row_repeater
                        model: root.column
                        property string chessboard_state: row_state
                        Rectangle {
                            id: chessSquare
                            height: root.row > root.column?  chessboard.height/root.row : width
                            width: root.row > root.column?  height:chessboard.width/root.column
                            radius: 1
                            property bool selected:(JSON.parse(row.square_selected))[index]
                            color: selected ?   index%2? firstColorSelected:secondColorSelected : index%2? firstColor:secondColor
                            property int _x: index
                            Image {
                                id: piece
                                anchors.fill: parent
                                source: (JSON.parse(row_repeater.chessboard_state))[index]
                                fillMode: Image.PreserveAspectFit
                                autoTransform: true
                                MouseArea{
                                    anchors.fill: parent
                                    onClicked: {
                                        var allSelections = JSON.parse(row.square_selected)
                                        if (allSelections[index] === true){
                                            allSelections[index] = false
                                        } else {
                                            allSelections[index] = true
                                        }
                                        columnModel.setProperty(_y,"square_selected", JSON.stringify(allSelections))
                                        focusItem.forceActiveFocus()
                                    }
                                }

                            }
                        }
                    }
                }
            }
        }
    }
    Rectangle{
        id: exportButton
        radius: 5
        color: "#333333"
        height: exportText.height
        width: exportText.width
        anchors{
            bottom: parent.bottom
            bottomMargin: height
            horizontalCenter: pieceSelection.horizontalCenter
        }

        Text{
            id: exportText
            text: "Export"
            font.pointSize: 36
            color:"black"
        }
        MouseArea{
            anchors.fill: parent
            onClicked: {
                console.log("export")
                var obstacles = []
                var kings = []
                var queens = []
                var bishops = []
                var rooks = []
                var knights = []
                for (var i = 0; i < columnModel.count; ++i){
                    var pieces = JSON.parse(columnModel.get(i).row_pieces)
                    for (var j = 0; j < pieces.length; ++j){
                        switch(pieces[j]){
                            case "obstacle":
                                obstacles.push(intToChar(j)+String(i))
                                break
                            case "king":
                                kings.push(intToChar(j)+String(i))
                                break
                            case "queen":
                                queens.push(intToChar(j)+String(i))
                                break
                            case "bishop":
                                bishops.push(intToChar(j)+String(i))
                                break
                            case "rook":
                                rooks.push(intToChar(j)+String(i))
                                break
                            case "knight":
                                knights.push(intToChar(j)+String(i))
                                break
                        }
                    }
                }
                var data = "Rows:" + String(root.row) +"\n" + "Cols:" + String(root.column) + "\nNumber of Obstacles:" + obstacles.length + "\nPosition of Obstacles (space between):"
                if (obstacles.length > 0){
                    for (var o in obstacles){
                        data += obstacles[o] + " "
                    }
                    data += "\n"
                } else {
                    data += "-\n"
                }
                data += "K (Minimum number of pieces left in goal):" + root.k + "\nNumber of King, Queen, Bishop, Rook, Knight (space between):"
                data += String(kings.length) + " " + String(queens.length) + " " + String(bishops.length) + " " + String(rooks.length) + " " + String(knights.length) + "\nPosition of Pieces [Piece, Pos]:\n"
                for (var i in kings){
                    data +="["+"King,"+kings[i]+"]\n"
                }
                for (var i in queens){
                    data +="["+"Queen,"+queens[i]+"]\n"
                }
                for (var i in bishops){
                    data +="["+"Bishop,"+bishops[i]+"]\n"
                }
                for (var i in rooks){
                    data +="["+"Rook,"+rooks[i]+"]\n"
                }
                for (var i in knights){
                    data +="["+"Knight,"+knights[i]+"]\n"
                }

                textFile.write(data)
            }
        }
    }
    Rectangle{
        id: resetButton
        radius: 5
        color: "#333333"
        height: resetText.height
        width: resetText.width
        anchors{
            bottom: exportButton.top
            bottomMargin: height
            horizontalCenter: exportButton.horizontalCenter
        }

        Text{
            id: resetText
            text: "Reset"
            font.pointSize: 36
            color:"black"
        }
        MouseArea{
            anchors.fill: parent
            onClicked: {
                console.log("reset")
                for (var i = 0; i < columnModel.count; ++i){
                    var r = []
                    var selected = []
                    var row_pieces = []
                    for (var j = 0; j < root.column; ++j){
                        r.push("")
                        selected.push(false)
                        row_pieces.push("")
                    }
                    columnModel.setProperty(i, "row_pieces", JSON.stringify(row_pieces))
                    columnModel.setProperty(i, "square_selected", JSON.stringify(selected))
                    columnModel.setProperty(i, "row_state", JSON.stringify(r))
                }
            }
        }
    }

    Rectangle{
        id: kBox
        height: resetButton.height
        width: resetButton.width*1.5
        color: "transparent"
        anchors{
            bottom: resetButton.top
            bottomMargin: height
            horizontalCenter: resetButton.horizontalCenter
        }
        Rectangle{
            id:kLabel
            anchors{
                top: kBox.top
                bottom: kBox.bottom
                left: kBox.left
            }
            width:kBox.width/3
            color:"transparent"
            Text{
                id: kText
                text: "K:"
                font.pointSize: 36
                color:"black"
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill:parent
            }
        }
        Rectangle{
            id: kInputBox
            anchors{
                top: kBox.top
                bottom: kBox.bottom
                right: kBox.right
                left: kLabel.right
            }
            color: resetButton.color
            radius: 2
            TextInput{
                id: kInput
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignLeft
                font.pointSize: 36
                leftPadding: kInputBox.width/10
                clip: true
            }
        }
    }

    Component.onCompleted: {
        for (var i = 0; i < root.row; ++i){
            var r = []
            var selected = []
            var row_pieces = []
            for (var j = 0; j < root.column; ++j){
                r.push("")
                selected.push(false)
                row_pieces.push("")
            }
            columnModel.append({
                                   "row_pieces": JSON.stringify(row_pieces),
                                   "square_selected": JSON.stringify(selected),
                                   "row_state": JSON.stringify(r)
                               })
        }

    }



}
