<template>
    <div class="login flexCenter">
        <header>
            <div class="logo ">
                <!-- <img src="../assets/images/logo.png" alt=""> -->
                <h2>人工智能不法信息识别系统</h2>
            </div>
        </header>
        <div class="verify">
            <div class="user">
                <div class="user_tips ">
                    <img src="../assets/images/user.png" alt="">
                    账号
                </div>
                <div class="ipt">
                    <input type="text" placeholder="请输入账号" v-model="username" @keyup.enter="submit">
                </div>
            </div>
            <div class="user" style="margin-top: 40px;">
                <div class="user_tips ">
                    <img src="../assets/images/password.png" alt="">
                    密码
                </div>
                <div class="ipt">
                    <input type="text" placeholder="请输入密码" v-model="password" @keyup.enter="submit">
                </div>
            </div>
            <div class="btn flexCenter" @click="onLogin">登录</div>
        </div>
    </div>
</template>
<script>
import qs from 'qs'
export default {
    data() {
        return {
            username: 'admin',
            password: 'admin'
        }
    },
    methods: {
        onLogin() {
            let data = { username: this.username, password: this.password }
            this.$axios.post("/login", qs.stringify(data)).then((res) => {
                if (res.status == 200) {
                    sessionStorage.setItem('user', JSON.stringify(res.data))
                        sessionStorage.setItem('token', res.data.access_token)
                    setTimeout(() => {
                        this.$message({
                            message: '登录成功',
                            type: 'success'
                        });
                        this.$router.push('./home')

                    }, 0);
                }
            })
        },

    }
}
</script>

