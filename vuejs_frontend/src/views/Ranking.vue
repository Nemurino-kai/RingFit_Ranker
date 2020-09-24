<template>
  <div class="ranking container">
    <h2 >Exercise Ranking</h2> <div class="text-muted">({{exercise_data.start_day}} 04:00:00 ～ {{exercise_data.stop_day}} 03:59:59)</div>
    <hr style="margin-top:0.5em;margin-bottom:1em;">
                <form class="form-group form-inline">
                        <label>集計日&nbsp;</label>
                        <input type="text" placeholder="Select Date.." name="day">
                        &nbsp;<button type="submit"  class="btn btn-primary">集計する</button>
                </form>

  <table class="table table-bordered">
    <thead>
      <tr><th>Rank</th><th>Username</th><th>kcal</th><th>Date</th></tr>
    </thead>
    <tbody>
      <tr v-for="user in exercise_data['exercise_data_list']" :key="user.id">
        <td>{{user.ranking}}</td>
        <td>{{user.user_name}}</td>
        <td>{{user.kcal}}</td>
        <td>{{user.tweeted_time}}</td>
      </tr>
    </tbody>
  </table>  </div>
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
    axios.get('https://ringfit.work/api').then(res => {
      this.exercise_data = res['data']
    })
  }
}
</script>
