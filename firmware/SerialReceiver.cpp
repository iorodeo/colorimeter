#include "Streaming.h"
#include "SerialReceiver.h"

SerialReceiver::SerialReceiver() {
    error = SR_ERR_NONE;
    resetState();
    startChar = SR_DFLT_START_CHAR;
    stopChar = SR_DFLT_STOP_CHAR;
    sepChar = SR_DFLT_SEP_CHAR;
    resetState();
}

bool SerialReceiver::messageReady() {
    if (state == SR_STATE_MESSAGE) {
        return true;
    }
    else {
        return false;
    }
}

uint8_t SerialReceiver::numberOfItems() {
    if (state == SR_STATE_MESSAGE) {
        return itemCnt;
    }
    else {
        return 0;
    }
}

char SerialReceiver::readChar(uint8_t itemNum, uint8_t ind) {
    char rval;
    if (checkItemRange(itemNum)) {
        if (ind < itemLenBuffer[itemNum]) {
            rval = itemBuffer[itemNum][ind];
        }
        else {
            rval = 0;
        }
    }
    else {
        rval = 0;
    }
    return rval;
}

int SerialReceiver::readInt(uint8_t itemNum) {
    if (checkItemRange(itemNum)) {
        return atoi(itemBuffer[itemNum]);
    }
    else {
        return 0;
    }
}

long SerialReceiver::readLong(uint8_t itemNum) {
    if (checkItemRange(itemNum)) {
        return atol(itemBuffer[itemNum]);
    }
    else {
        return 0;
    }
}

double SerialReceiver::readDouble(uint8_t itemNum) {
    if(checkItemRange(itemNum)) {
        return atof(itemBuffer[itemNum]);
    }
    else {
        return 0;
    }
}

float SerialReceiver::readFloat(uint8_t itemNum) {
    return (float) readDouble(itemNum);
}

void SerialReceiver::copyString(uint8_t itemNum, char* string, uint8_t size) {
    if (checkItemRange(itemNum)) {
        strlcpy(string,itemBuffer[itemNum],size);
    }
    else {
        if (size >= 0) {
            string[0] = '\0';
        }
    }
}


bool SerialReceiver::checkItemRange(uint8_t itemNum) {
    if ((state==SR_STATE_MESSAGE) && (itemNum >=0) && (itemNum < itemCnt)) {
        return true;
    }
    else {
        return false;
    }
}

void SerialReceiver::process(int serialByte) {
    if (serialByte > 0){
        switch (state) {
            case SR_STATE_IDLE:
                processNewMsg(serialByte);
                break;
            case SR_STATE_RECEIVING:
                processCurMsg(serialByte);
                break;
            case SR_STATE_MESSAGE:
                break;
            default:
                break;

        }
    }
}

void SerialReceiver::processNewMsg(int serialByte) {
    if (serialByte == startChar) {
        resetItems();
        state = SR_STATE_RECEIVING;
        error = SR_ERR_NONE;
    }
    else if ((serialByte == '\n') || (serialByte == ' ')) {
        return;
    }
    else {
        error = SR_ERR_ILLEGAL_CHAR;
        resetState();
    }
}

void SerialReceiver::processCurMsg(int serialByte) {
    if (serialByte == startChar) {
        handleStartChar(serialByte);
    }
    else if (serialByte == stopChar) {
        handleStopChar(serialByte);
    }

    else if (serialByte == sepChar) {
        handleSepChar(serialByte);
    }

    else {
        handleNewChar(serialByte);
    }
}

void SerialReceiver::handleStartChar(int serialByte) {
    resetState();
    error = SR_ERR_ILLEGAL_CHAR;
}

void SerialReceiver::handleStopChar(int serialByte) {
    if (itemPos > 0) {
        itemBuffer[itemCnt][itemPos] = '\0';
        itemLenBuffer[itemCnt] = itemPos;
        itemCnt++;
    }
    // Check message checksum here .... if not OK reset.
    state = SR_STATE_MESSAGE;
}

void SerialReceiver::handleSepChar(int serialByte) {
    if (itemPos > 0) {
        if (itemCnt == SR_MAX_ITEMS-1) {
            resetState();
            error = SR_ERR_MESSAGE_LENGTH;
        }
        else {
            itemBuffer[itemCnt][itemPos] = '\0';
            itemLenBuffer[itemCnt] = itemPos;
            itemCnt++;
            itemPos = 0;
        }
    }
    else {
        resetState();
        error = SR_ERR_ITEM_LENGTH;
    }
}

void SerialReceiver::handleNewChar(int serialByte) {
    if (itemPos == SR_MAX_ITEM_SZ) {
        resetState();
        error = SR_ERR_ITEM_LENGTH;
    }
    else {
        if ((serialByte == '\n') || (serialByte == ' ')) {
            return;
        }
        itemBuffer[itemCnt][itemPos] = serialByte;
        itemPos++;
    }
}

void SerialReceiver::reset() {
    resetState();
    error = SR_ERR_NONE;
}

void SerialReceiver::resetState() {
    resetItems();
    state = SR_STATE_IDLE;
}

void SerialReceiver::resetItems() {
    itemCnt = 0;
    itemPos = 0;
    for (int i=0; i<SR_MAX_ITEMS;i++) {
        itemBuffer[i][0] = '\0';
        itemLenBuffer[i] = 0;
    }
}

void SerialReceiver::printInfo() {
    Serial << "Current Message Info" << endl;
    Serial << "--------------------" << endl;
    Serial << "state:   " << _DEC(state) << endl;
    Serial << "error:   " << _DEC(error) << endl;
    Serial << "itemCnt: " << _DEC(itemCnt) << endl;
    Serial << "itemPos: " << _DEC(itemPos) << endl;
    for (int i=0; i<itemCnt; i++) {
        Serial << "buf[" << _DEC(i) << "] = " << itemBuffer[i] << endl;
    }
    Serial << endl;
}

void SerialReceiver::printMessageInfo() {
    Serial << "Message = " << endl;
    for (int i=0; i<itemCnt; i++) {
        Serial << "buf[" << _DEC(i) << "] = " << itemBuffer[i] << ", len = " << _DEC(itemLenBuffer[i]) << endl;
    }
    Serial << endl;
}

void SerialReceiver::printMessage() {
    for (int i=0; i<itemCnt; i++) {
        if (i < itemCnt-1) {
            Serial << itemBuffer[i] << " ";
        }
        else {
            Serial << itemBuffer[i];
        }
    }
    Serial << endl;
}
