import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import React, { useState, useEffect} from 'react';

export function Navigation() {
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('access_token') !== null) {
      setIsAuth(true);
    }
  }, []);

  return (
    <Navbar className='navbar'>
        <Container>
            <Navbar.Brand href="/">
              <img
                src="/logo.svg"
                width="30"
                height="30"
                className="d-inline-block align-top"
                alt="React Bootstrap logo"
              />
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="responsive-navbar-nav" />
            <Navbar.Collapse id="responsive-navbar-nav">
              <Nav className="me-auto">
              </Nav>
              <Nav>
                {isAuth ? (
                  <Nav.Link href="/logout" className="auth-link">退出登录</Nav.Link>
                ) : (
                  <>
                    <Nav.Link href="/login" className="auth-link">登录</Nav.Link>
                    <Nav.Link href='/register' className="auth-link">注册</Nav.Link>
                  </>
                )}
              </Nav>              
            </Navbar.Collapse>
        </Container>
    </Navbar>
  );
}

export default Navigation