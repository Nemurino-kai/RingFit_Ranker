<template>
  <div class="user container">
  <h1>いままでの運動記録</h1>
      <hr style="margin-top:0.5em;margin-bottom:1em;">
                <form class="form-group form-inline">
                        <label>ユーザ名&nbsp;</label>
                        <input type="text" placeholder="Input Username ..." name="user">
                        &nbsp;<button type="submit"  class="btn btn-primary">集計する</button>
                </form>
  <table class="table table-bordered">
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
import axios from 'axios'

export default {
  data () {
    return {
      exercise_data: []
    }
  },
  mounted () {
    axios.get('https://ringfit.work/api/user?user=aipQKAgOzRwoYGl').then(res => {
      this.exercise_data = res['data']
    })
  }
}
</script>
