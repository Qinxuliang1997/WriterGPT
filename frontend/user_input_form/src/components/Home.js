import React from 'react';
import ScrollReveal from 'scrollreveal';
import VanillaTilt from 'vanilla-tilt';

class Portfolio extends React.Component {
    componentDidMount() {
        this.initScrollReveal();
        this.initTilt();
    }

    initScrollReveal() {
        const defaultProps = {
            easing: 'cubic-bezier(0.5, 0, 0, 1)',
            distance: '30px',
            duration: 1000,
            desktop: true,
            mobile: true
        };

        const targetElements = [
            {
                element: '.section-title',
                animation: {
                    delay: 300,
                    distance: '0px',
                    origin: 'bottom'
                },
            },
            {
                element: '.hero-title',
                animation: {
                    delay: 500,
                    origin: window.innerWidth > 768 ? 'left' : 'bottom',
                },
            },
            {
                element: '.hero-cta',
                animation: {
                    delay: 1000,
                    origin: window.innerWidth > 768 ? 'left' : 'bottom',
                },
            },
            {
                element: '.about-wrapper__image',
                animation: {
                    delay: 600,
                    origin: 'bottom'
                },
            },
            {
                element: '.about-wrapper__info',
                animation: {
                    delay: 1000,
                    origin: window.innerWidth > 768 ? 'left' : 'bottom',
                },
            },
            {
                element: '.project-wrapper__text',
                animation: {
                    delay: 500,
                    origin: window.innerWidth > 768 ? 'left' : 'bottom',
                },
            },
            {
                element: '.project-wrapper__image',
                animation: {
                    delay: 1000,
                    origin: window.innerWidth > 768 ? 'right' : 'bottom',
                },
            },
            {
                element: '.contact-wrapper',
                animation: {
                    delay: 800,
                    origin: 'bottom'
                },
            }
        ];

        // Initialize all the scroll reveal animations
        targetElements.forEach(({ element, animation }) => {
            ScrollReveal().reveal(element, {...defaultProps, ...animation});
        });
    }

    initTilt() {
        // Initialize tilt animations on specified elements
        VanillaTilt.init(document.querySelectorAll(".js-tilt"), {
            max: 25,
            speed: 400,
            glare: true,
            "max-glare": 0.5
        });
    }

    render() {
        return (
            <div id="top">
                <section id="hero" className="jumbotron">
                    <div className="container">
                        <h1 className="hero-title load-hidden">
                            嗨！欢迎来到 <span className="text-color-main">万卷公文</span>
                            <br />
                            AI速成公文，基于素材定制，告别空无一物
                        </h1>
                        <p className="hero-cta load-hidden">
                            <a className="cta-btn cta-btn--hero" href="#about">了解更多</a>
                        </p>
                    </div>
                </section>
                <section id="about">
                    <div className="container">
                        <h2 className="section-title load-hidden">关于万卷公文</h2>
                        <div className="row about-wrapper">
                            <div className="col-md-6 col-sm-12">
                                <div className="about-wrapper__info load-hidden">
                                    <p className="about-wrapper__info-text">
                                        万卷公文是一个方便快捷的在线文字材料处理平台，超强AI能力支撑，直击公文写作痛点！
                                    </p>
                                    <span className="d-flex mt-3">
                                        <a className="cta-btn cta-btn--resume" href="/login">
                                            免费使用
                                        </a>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                <section id="projects">
                    <div className="container">
                        <h2 className="section-title dark-blue-text">核心能力</h2>
                        <div className="project-wrapper">
                            <div className="row">
                                <div className="col-lg-4 col-sm-12">
                                    <div className="project-wrapper__text load-hidden">
                                        <h3 className="project-wrapper__text-title">保护你的数据安全</h3>
                                        <p>对数据进行向量化处理，用完即删</p>
                                    </div>
                                </div>
                                <div className="col-lg-4 col-sm-12">
                                    <div className="project-wrapper__text load-hidden">
                                        <h3 className="project-wrapper__text-title">告别假大空</h3>
                                        <p>根据素材定制公文，拒绝空洞</p>
                                    </div>
                                </div>
                                <div className="col-lg-4 col-sm-12">
                                    <div className="project-wrapper__text load-hidden">
                                        <h3 className="project-wrapper__text-title">好公文是改出来的</h3>
                                        <p>句子级的AI更改，让你轻松掌控细节</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                <section id="contact">
                    <div className="container">
                        <h2 className="section-title">联系我们</h2>
                        <div class="contact-wrapper load-hidden">
                            <p className="contact-wrapper__text">205989421@qq.com</p>
                            <a className="cta-btn cta-btn--resume" href="mailto:example@email.com">发送邮件</a>
                        </div>
                    </div>
                </section>
                <footer className="footer navbar-static-bottom">
                    <div className="container">
                        <a href="#top" className="back-to-top">
                            <i className="fa fa-angle-up fa-2x" aria-hidden="true"></i>
                        </a>
                        <hr />
                        <p className="footer__text">
                            © 2024 - Developed by 
                            <a href="https://qinxuliang1997.github.io" target="_blank"> XL Q</a>
                        </p>
                    </div>
                </footer>
            </div>
        );
    }
}

export default Portfolio;
