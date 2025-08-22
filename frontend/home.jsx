import React from 'react';
import { FlatList, Image, ScrollView, StyleSheet, Text, TouchableOpacity, useWindowDimensions, View } from 'react-native';

// --- Sample Data ---
const userProfile = {
  name: 'Jeremy Barrera',
  title: 'React Native Developer | AmenLink',
  avatar: `https://i.pravatar.cc/150?u=jeremy`,
  connections: 150,
  views: 88,
};

const feedData = [
  {
    id: '1',
    author: 'GitHub Copilot',
    title: 'AI in Development',
    avatar: `https://i.pravatar.cc/150?u=copilot`,
    content: 'AI is transforming the way we build software. With tools like GitHub Copilot, developers can write code faster, with fewer errors, and focus more on solving complex problems.',
    likes: 120,
    comments: 45,
  },
  {
    id: '2',
    author: 'React Native Team',
    title: 'Staff Engineer at Meta',
    avatar: `https://i.pravatar.cc/150?u=react`,
    content: 'The latest version of React Native brings significant performance improvements to the new architecture. Have you migrated your app yet? Share your experience in the comments!',
    likes: 543,
    comments: 102,
  },
];

const newsData = [
    { id: '1', title: 'Tech hiring sees an uptick' },
    { id: '2', title: 'The future of remote work' },
    { id: '3', title: 'AI regulation talks heat up' },
    { id: '4', title: 'Top skills for developers in 2025' },
];


// --- UI Components ---

const ProfileCard = ({ user }) => (
  <View style={styles.card}>
    <Image source={{ uri: user.avatar }} style={styles.profileAvatar} />
    <Text style={styles.profileName}>{user.name}</Text>
    <Text style={styles.profileTitle}>{user.title}</Text>
    <View style={styles.divider} />
    <View style={styles.profileStats}>
        <Text style={styles.statText}>Connections: {user.connections}</Text>
        <Text style={styles.statText}>Profile Views: {user.views}</Text>
    </View>
  </View>
);

const PostCard = ({ post }) => (
    <View style={[styles.card, { marginBottom: 10 }]}>
        <View style={styles.postHeader}>
            <Image source={{ uri: post.avatar }} style={styles.postAvatar} />
            <View>
                <Text style={styles.postAuthor}>{post.author}</Text>
                <Text style={styles.postAuthorTitle}>{post.title}</Text>
            </View>
        </View>
        <Text style={styles.postContent}>{post.content}</Text>
        <View style={styles.divider} />
        <View style={styles.postActions}>
            <TouchableOpacity style={styles.actionButton}><Text>Like</Text></TouchableOpacity>
            <TouchableOpacity style={styles.actionButton}><Text>Comment</Text></TouchableOpacity>
            <TouchableOpacity style={styles.actionButton}><Text>Share</Text></TouchableOpacity>
        </View>
    </View>
);

const NewsCard = ({ news }) => (
    <View style={styles.card}>
        <Text style={styles.newsTitle}>AmenLink News</Text>
        {news.map(item => (
            <TouchableOpacity key={item.id} style={styles.newsItem}>
                <Text style={styles.newsItemText}>• {item.title}</Text>
            </TouchableOpacity>
        ))}
    </View>
);


// --- Main Home Component ---

const home = () => {
  const { width } = useWindowDimensions();
  const isDesktop = width > 768;

  return (
    <ScrollView style={styles.container}>
      <View style={[styles.main, isDesktop && styles.mainDesktop]}>
        
        {/* Left Column */}
        {isDesktop && (
            <View style={styles.leftColumn}>
                <ProfileCard user={userProfile} />
            </View>
        )}

        {/* Center Column (Feed) */}
        <View style={styles.centerColumn}>
            {!isDesktop && <ProfileCard user={userProfile} />}
            <FlatList
                data={feedData}
                renderItem={({ item }) => <PostCard post={item} />}
                keyExtractor={item => item.id}
                scrollEnabled={false} // Disable FlatList scrolling within ScrollView
            />
        </View>

        {/* Right Column */}
        {isDesktop && (
            <View style={styles.rightColumn}>
                <NewsCard news={newsData} />
            </View>
        )}
      </View>
    </ScrollView>
  );
};

// --- Styles ---

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f3f2ef',
  },
  main: {
    padding: 10,
  },
  mainDesktop: {
    flexDirection: 'row',
    justifyContent: 'center',
    maxWidth: 1128,
    marginHorizontal: 'auto',
  },
  leftColumn: {
    width: 225,
    marginRight: 20,
  },
  centerColumn: {
    flex: 1,
    maxWidth: 555,
  },
  rightColumn: {
    width: 300,
    marginLeft: 20,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 8,
    padding: 15,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  divider: {
    height: 1,
    backgroundColor: '#e0e0e0',
    marginVertical: 10,
  },
  // Profile Card
  profileAvatar: {
    width: 72,
    height: 72,
    borderRadius: 36,
    alignSelf: 'center',
    marginBottom: 10,
  },
  profileName: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  profileTitle: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 10,
  },
  profileStats: {
    alignItems: 'flex-start',
  },
  statText: {
    fontSize: 12,
    color: '#666',
    marginBottom: 5,
  },
  // Post Card
  postHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  postAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    marginRight: 10,
  },
  postAuthor: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  postAuthorTitle: {
    fontSize: 12,
    color: '#666',
  },
  postContent: {
    fontSize: 14,
    lineHeight: 20,
  },
  postActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    padding: 8,
  },
  // News Card
  newsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  newsItem: {
    paddingVertical: 5,
  },
  newsItemText: {
    fontSize: 14,
    color: '#333',
  },
});

export default home;