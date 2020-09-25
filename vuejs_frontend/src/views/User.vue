<template>
  <div class="user container">
  <h1>いままでの運動記録</h1>
      <hr style="margin-top:0.5em;margin-bottom:1em;">
                <form class="form-group form-inline">
                        <label>ユーザ名&nbsp;</label>
                        <input type="text" placeholder="Input Username ..." v-model="user" name="user">
                        &nbsp;<router-link v-bind:to="'/user/' + user" class="btn btn-primary">集計する</router-link>
                </form>
  <table class="table table-bordered" v-if="exercise_data.length != 0">
    <thead>
      <tr><th>Rank</th><th>kcal</th><th>Date</th></tr>
    </thead>
    <tbody>
      <tr v-for="user in exercise_data['user_exercise_data_list']" :key="user.id">
        <td>{{user.daily_rank}}</td>
        <td>{{user.kcal}}</td>
        <td>{{user.tweeted_time}}</td>
      </tr>
    </tbody>
  </table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      user: '',
      exercise_data: []
    }
  },
  created: function () {
    if (this.$route.params.Username != null) {
      this.$api.get('https://ringfit.work/api/user?user=' + this.$route.params.Username).then(res => {
        this.exercise_data = res['data']
      })
    }
  },
  watch: {
    $route (to, from) {
      this.$api.get('https://ringfit.work/api/user?user=' + this.$route.params.Username).then(res => {
        this.exercise_data = res['data']
      })
    }
  }
}
</script>
