import React from 'react';
// Import useWindowDimensions instead of Dimensions
import { StyleSheet, Text, TouchableOpacity, View, useWindowDimensions } from 'react-native';


const initial = () => {
    // Get width from the hook inside the component
    const { width } = useWindowDimensions();
    const isSmallScreen = width < 800; 

    return (
        <View style={styles.container}>
            {/* The width will now update on resize */}
            <TouchableOpacity style={[styles.button, { width: isSmallScreen ? '60%' : '30%' }]}>
                <Text style={styles.buttonText}>Find Churches</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.button, styles.loginButton, { width: isSmallScreen ? '60%' : '30%' }]}>
                <Text style={styles.buttonText}>Login</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.button, styles.signupButton, { width: isSmallScreen ? '60%' : '30%' }]}>
                <Text style={styles.buttonText}>Signup</Text>
            </TouchableOpacity>
        </View>
    );
};


const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 20,
        marginTop: 50, // Adjusted for better visibility
        paddingVertical: 0,
    },
    button: {
        backgroundColor: '#6200ee', // Default purple color
        paddingVertical: 15,
        paddingHorizontal: 30,
        borderRadius: 25, // This makes the button rounded
        marginVertical: 10,
        alignItems: 'center',
    },
    loginButton: {
        backgroundColor: '#03DAC6', // Teal color for login
    },
    signupButton: {
        backgroundColor: '#018786', // Darker teal for signup
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
});


export default initial