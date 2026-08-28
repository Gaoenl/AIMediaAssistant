package com.aima.auth.service;

import com.aima.auth.dto.LoginRequest;
import com.aima.auth.dto.LoginResponse;

/** 认证服务接口 */
public interface AuthService {

    /** 登录校验,成功返回 JWT */
    LoginResponse login(LoginRequest request);
}