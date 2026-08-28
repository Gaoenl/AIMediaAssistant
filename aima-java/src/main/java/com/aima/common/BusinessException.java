package com.aima.common;

public class BusinessException extends RuntimeException {
    private final int status;
    private final int code;

    public BusinessException(int status, String message) {
        super(message);
        this.status = status;
        this.code = status;
    }

    public int getStatus() { return status; }
    public int getCode() { return code; }
}