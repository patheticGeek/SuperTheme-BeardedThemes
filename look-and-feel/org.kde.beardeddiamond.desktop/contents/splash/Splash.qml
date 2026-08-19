import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    color: "#111418"

    property int stage

    onStageChanged: {
        if (stage == 2) {
            introAnimation.running = true;
        } else if (stage == 5) {
            introAnimation.target = busyIndicator;
            introAnimation.from = 1;
            introAnimation.to = 0;
            introAnimation.running = true;
        }
    }

    Item {
        id: content
        anchors.fill: parent
        opacity: 0

        Image {
            id: logo
            readonly property real size: Kirigami.Units.gridUnit * 8

            anchors.centerIn: parent

            asynchronous: true
            source: "images/logo.png"

            sourceSize.width: size
            sourceSize.height: size
        }

        Image {
            id: busyIndicator
            y: parent.height - (parent.height - logo.y) / 2 - height / 2
            anchors.horizontalCenter: parent.horizontalCenter
            asynchronous: true
            source: "images/spinner.png"
            sourceSize.height: Kirigami.Units.gridUnit * 2
            sourceSize.width: Kirigami.Units.gridUnit * 2
            RotationAnimator on rotation {
                id: rotationAnimator
                from: 0
                to: 360
                duration: 1400
                loops: Animation.Infinite
                running: Kirigami.Units.longDuration > 1
            }
        }

        Text {
            anchors {
                bottom: parent.bottom
                right: parent.right
                margins: Kirigami.Units.gridUnit
            }
            color: "#bec6d0"
            text: "Bearded Diamond"
            Accessible.name: text
            Accessible.role: Accessible.StaticText
            textFormat: Text.PlainText
        }
    }

    OpacityAnimator {
        id: introAnimation
        running: false
        target: content
        from: 0
        to: 1
        duration: Kirigami.Units.veryLongDuration * 2
        easing.type: Easing.InOutQuad
    }
}
