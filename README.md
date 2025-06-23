# 🔎 FindIt

A **Flask-based Lost & Found System** designed for campus environments. It enables users to seamlessly post, browse, and retrieve lost/found items—bridging the gap between finders and seekers with real-time updates, image uploads, and profile management.

---

## 🚀 Key Features

- 🔐 **Secure Auth**: Firebase Authentication for Signup/Login  
- 📝 **Post System**: Create Lost/Found item posts with images, timestamps & location  
- 📷 **Image Upload**: Integrated with **Cloudinary** for scalable image handling  
- 🗺️ **Personal Dashboard**: View and manage your personal posts  
- ⏱️ **Sorted Feed**: Feed sorted by time (newest first)  
- 🔒 **Session Management**: Ensures only logged-in users can access core features  

---

## ⚙️ Tech Stack

| Area              | Tools Used                           |
|------------------|--------------------------------------|
| **Backend**       | Python, Flask                        |
| **Authentication**| Firebase Authentication              |
| **Database**      | Firebase Realtime Database           |
| **Image Hosting** | Cloudinary                           |
| **Environment**   | Python-dotenv for secrets handling   |
| **Frontend**      | HTML, Jinja2 Templates               |
| **Deployment-Ready** | Clean structure for scaling and integration |

---

## 🛠️ Architecture

1. **User Auth** via Firebase  
2. **Post Creation** → Cloudinary (image) + Firebase DB (text)  
3. **Real-time Feed** → `home()` fetches and sorts posts  
4. **User Profile** → Filtered posts + delete option  
5. **Session Handling** → Uses Flask session securely  

---

## 🖼️ UI Snapshots 

> - Signup/Login ![Screenshot 2025-06-23 at 5 05 37 PM](https://github.com/user-attachments/assets/424c8cb9-c61f-4550-8693-4a9c01abfe77)

> - Post form  ![Screenshot 2025-06-23 at 5 05 01 PM](https://github.com/user-attachments/assets/d05f8ff9-5c2b-4cd7-b857-1741584a82ac)

> - Feed of posts ![Screenshot 2025-06-23 at 5 04 40 PM](https://github.com/user-attachments/assets/0ae89512-c99b-43f6-aa85-00aefc3ea208)

> - Profile page with delete option ![Screenshot 2025-06-23 at 5 05 20 PM](https://github.com/user-attachments/assets/5c9c9397-afae-41c1-afd3-3553e835f3a5)


---

## 🧠 Future Enhancements

- 🔍 AI-powered image & text similarity for matching lost & found items  
- 📍 Location heatmaps for smart suggestions  
- 📲 Push notifications for nearby matches  

