package com.aima.auth.dto;

/** 登录响应:返回 JWT 与用户名 */
public record LoginResponse(String token, String username) {
}