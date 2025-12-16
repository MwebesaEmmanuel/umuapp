import 'package:dio/dio.dart';

class AuthApi {
  AuthApi(this._dio);

  final Dio _dio;

  Future<String> register({required String email, required String password}) async {
    final resp = await _dio.post<Map<String, dynamic>>(
      '/auth/register',
      data: {'email': email, 'password': password},
    );
    return resp.data?['access_token'] as String;
  }

  Future<String> login({required String email, required String password}) async {
    final resp = await _dio.post<Map<String, dynamic>>(
      '/auth/login',
      data: {'email': email, 'password': password},
    );
    return resp.data?['access_token'] as String;
  }

  Future<Map<String, dynamic>> me() async {
    final resp = await _dio.get<Map<String, dynamic>>('/users/me');
    return resp.data ?? <String, dynamic>{};
  }
}

