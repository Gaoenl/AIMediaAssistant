package com.aima.auth.service.impl;

import com.aima.auth.dto.LoginRequest;
import com.aima.auth.dto.LoginResponse;
import com.aima.auth.service.AuthService;
import com.aima.common.BusinessException;
import com.aima.security.JwtUtil;
import org.springframework.stereotype.Service;

/**
 * 认证服务实现。
 * M1:固定账号 admin/123456,M2 替换为 MySQL 用户表 + BCrypt 校验。
 */
@Service
public class AuthServiceImpl implements AuthService {

    private final JwtUtil jwtUtil;

    public AuthServiceImpl(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @Override
    public LoginResponse login(LoginRequest request) {
        if (!"admin".equals(request.username()) || !"123456".equals(request.password())) {
            throw new BusinessException(401, "用户名或密码错误");
        }
        return new LoginResponse(jwtUtil.generate(request.username()), request.username());
    }
}