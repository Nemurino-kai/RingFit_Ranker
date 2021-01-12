<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand to="/">RingFitRanker</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item to="/">Ranking</b-nav-item>
        <b-nav-item :to="'/user/' + this.$store.state.userRank.user">User</b-nav-item>
        <b-nav-item to="/about">About</b-nav-item>
        <b-nav-item to="/questions">Q&A</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  <br>
</div>
</template>
