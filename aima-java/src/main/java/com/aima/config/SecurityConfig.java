package com.aima.config;

import com.aima.security.JwtAuthFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;

/**
 * Spring Security 配置:无状态 JWT。
 *
 * <p>说明:requestMatchers 不使用字符串重载,而显式构造 {@link AntPathRequestMatcher}。
 * Spring Security 6 中字符串形式的 requestMatchers 需要依赖 Spring MVC 的
 * HandlerMappingIntrospector 来判断匹配器类型;在部分环境(单元测试、非 MVC 上下文等)下
 * 会抛出 "This method cannot decide whether these patterns are Spring MVC patterns or not",
 * 显式指定匹配器可消除该歧义,行为也完全一致。
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity   // 预留 @PreAuthorize 等方法级鉴权(M2 RBAC 使用)
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http, JwtAuthFilter jwtAuthFilter) throws Exception {
        http.csrf(AbstractHttpConfigurer::disable)
                // 无状态:不创建 Session
                .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(a -> a
                        // 白名单:登录、Java↔Python 内部接口、错误页
                        .requestMatchers(
                                new AntPathRequestMatcher("/api/v1/auth/login"),
                                new AntPathRequestMatcher("/internal/**"),
                                new AntPathRequestMatcher("/error"))
                        .permitAll()
                        // 其余接口必须携带有效 JWT
                        .anyRequest().authenticated())
                // JWT 过滤器放在用户名密码过滤器之前
                .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }
}