import axios from "axios";

class AppService {
  async predict(data) {
    try {
      var result = await axios.post('/api', data, {
        headers: {
          "Content-Type": "multipart/form-data",
        }
      })
      return result.data;
    } catch (error) {
      return null;
    }
  }
}

export default new AppService();