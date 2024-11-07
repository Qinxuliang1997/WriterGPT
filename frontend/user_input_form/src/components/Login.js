import axios from "axios";
import { useState } from "react";

export const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const submit = async e => {
        e.preventDefault();

        const user = {
            username: username,
            password: password
        };

        try {
            // localhost:8000
            const { data } = await axios.post('http://106.14.184.241/token/', user, {
                headers: {
                    'Content-Type': 'application/json'
                },
                withCredentials: true
            });

            localStorage.clear();
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            localStorage.setItem('user_name', username);
            axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
            window.location.href = '/start';
        } catch (error) {
            if (error.response && error.response.status === 401) {
                setError('用户名或密码错误');
            } else {
                setError('用户名或密码错误');
            }
        }
    };

    return (
        <div className="Auth-form-container">
            <form className="Auth-form" onSubmit={submit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">登录</h3>
                    {error && <div className="alert alert-danger" role="alert">{error}</div>}
                    <div className="form-group mt-3">
                        <label>用户名</label>
                        <input
                            className="form-control mt-1"
                            // placeholder="输入用户名"
                            name='username'
                            type='text'
                            value={username}
                            required
                            onChange={e => setUsername(e.target.value)}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>密码</label>
                        <input
                            name='password'
                            type="password"
                            className="form-control mt-1"
                            // placeholder="输入密码"
                            value={password}
                            required
                            onChange={e => setPassword(e.target.value)}
                        />
                    </div>
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary">
                            提交
                        </button>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default Login;
