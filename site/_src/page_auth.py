auth_css = """<style>
.auth{min-height:calc(100vh - 80px);display:grid;place-items:center;padding:40px 0}
.auth .box{width:min(440px,100%);padding:36px}
.auth .box h2{font-size:28px;margin-bottom:6px;max-width:none}
.auth .box .sub{color:var(--ink-2);margin-bottom:24px}
.auth .logo{display:inline-flex;align-items:center;gap:10px;font:700 22px var(--font-display);letter-spacing:-.04em;color:var(--abyss);text-decoration:none;margin-bottom:26px}
.auth .logo img{width:34px}
.auth .alt{margin-top:18px;font-size:14px;color:var(--ink-3);text-align:center}
.auth .or{display:flex;align-items:center;gap:12px;color:var(--ink-3);font-size:13px;margin:16px 0}
.auth .or::before,.auth .or::after{content:"";flex:1;height:1px;background:var(--glass-line)}
.demo{margin-top:14px;padding:12px 14px;border-radius:14px;background:rgba(59,91,255,.08);font-size:13px;color:var(--ink-2)}
</style>"""

login = """<main class="auth"><div class="wrap" style="display:grid;justify-items:center"><div class="box glass strong">
  <a class="logo" href="index.html"><img src="assets/mark.svg" alt="">transiqe</a>
  <h2>Sign in to your business</h2><p class="sub">Your dashboard, invoices, customers and autopay.</p>
  <form action="https://app.transiqe.com/login" method="post">
    <label class="field"><span>Work email</span><input type="email" name="email" placeholder="you@yourbusiness.com.au" autocomplete="email" required></label>
    <label class="field"><span>Password</span><input type="password" name="password" autocomplete="current-password" required></label>
    <div style="display:flex;justify-content:space-between;align-items:center;margin:4px 0 18px"><label class="check" style="font-size:13.5px"><input type="checkbox" name="remember"> <span>Keep me signed in</span></label><a href="#" class="small">Forgot password?</a></div>
    <button class="btn primary block lg">Sign in</button>
  </form>
  <div class="or">or</div>
  <a class="btn glassy block" href="portal.html">I'm a customer paying an invoice</a>
  <p class="alt">New to Transiqe? <a href="signup.html">Create a business account</a></p>
</div></div></main>"""

signup = """<main class="auth"><div class="wrap" style="display:grid;justify-items:center"><div class="box glass strong" style="width:min(520px,100%)">
  <a class="logo" href="index.html"><img src="assets/mark.svg" alt="">transiqe</a>
  <h2>Create your business account</h2><p class="sub">Free while you set up. No card needed to start.</p>
  <form action="https://app.transiqe.com/signup" method="post">
    <label class="field"><span>Business name</span><input name="name" placeholder="e.g. Northside Physio Pty Ltd" required></label>
    <div class="grid c2" style="gap:12px">
      <label class="field"><span>Your name</span><input name="owner_name" required></label>
      <label class="field"><span>ABN (optional)</span><input name="abn" inputmode="numeric"></label>
    </div>
    <label class="field"><span>Work email</span><input type="email" name="email" autocomplete="email" required></label>
    <label class="field"><span>Password</span><input type="password" name="password" autocomplete="new-password" minlength="8" required><span class="tiny muted" style="font-weight:500">At least 8 characters</span></label>
    <label class="check" style="margin:6px 0 18px"><input type="checkbox" required> <span>I agree to the <a href="#">terms</a> and <a href="#">privacy policy</a>.</span></label>
    <button class="btn primary block lg">Create account</button>
  </form>
  <div class="demo">What happens next: connect Xero (two minutes), add the gateway details from NAB when they arrive, paste one link into Xero. Your first invoice can go out the same day.</div>
  <p class="alt">Already have an account? <a href="login.html">Sign in</a></p>
</div></div></main>"""

portal = """<main class="auth"><div class="wrap" style="display:grid;justify-items:center"><div class="box glass strong">
  <a class="logo" href="index.html"><img src="assets/mark.svg" alt="">transiqe</a>
  <h2>Customer portal</h2><p class="sub">Enter the email your invoices are sent to and we'll email you a secure sign-in link. No password needed.</p>
  <form action="https://app.transiqe.com/portal/request-link" method="post">
    <label class="field"><span>Email</span><input type="email" name="email" placeholder="you@example.com" autocomplete="email" required></label>
    <button class="btn primary block lg">Email me a sign-in link</button>
  </form>
  <p class="alt">In the portal you can see every invoice, pay by card, and manage automatic payments and saved cards for the business that invoices you.</p>
  <p class="alt">Running a business? <a href="login.html">Business sign in</a></p>
</div></div></main>"""

page('login', 'Sign in · Transiqe', 'Sign in to your Transiqe business account.', login, extra_css=auth_css)
page('signup', 'Create an account · Transiqe', 'Create a Transiqe business account and connect Xero to your bank gateway.', signup, extra_css=auth_css)
page('portal', 'Customer portal · Transiqe', 'Sign in to view and pay your invoices and manage automatic payments.', portal, extra_css=auth_css)
