import React from 'react';

function HeroSection() {
    return (
        <section id="hero" className="jumbotron">
            <div className="container">
                <h1 className="hero-title load-hidden">
                    嗨！欢迎来到 <span className="text-color-main">万卷公文</span>
                    <br />
                    AI速成公文，基于素材定制，告别空无一物
                </h1>
                <p className="hero-cta load-hidden">
                    <a rel="noreferrer" className="cta-btn cta-btn--hero" href="login">免费开始</a>
                </p>
            </div>
        </section>
    );
}

export default HeroSection;
