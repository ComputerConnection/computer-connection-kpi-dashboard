import { GraphQLClient } from 'graphql-request';

const endpoint = '/graphql';

const client = new GraphQLClient(endpoint);

export async function gql<T>(query: string, variables?: Record<string, any>): Promise<T> {
  return client.request<T>(query, variables);
}
